from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .models import db, User, Recipe
from .forms import LoginForm, RegisterForm, RecipeForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import myapp_obj
from datetime import datetime

# Login Page
@myapp_obj.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

# User Registration
@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.')
            return render_template('register.html', form=form)

        # creates a new user w hashed password
        hashed_pw = generate_password_hash(form.password.data, method='scrypt')
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
	
# Displays Recipes
@myapp_obj.route('/home')
@login_required # only accessible to logged in users
def home():
	recipes = Recipe.query.order_by(Recipe.created.desc()).all()
	return render_template('home.html', recipes=recipes)

# Logout User	
@myapp_obj.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

# Lists Recipes
@myapp_obj.route("/recipes")
def list_recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)

# Add New Recipe
@myapp_obj.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            created=datetime.utcnow()
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added successfully!')
    return render_template("add_recipe.html", form=RecipeForm())

# Recipe Detail
@myapp_obj.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)

# Deletes Recipe
@myapp_obj.route("/recipe/<int:recipe_id>/delete")
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted.')
    return redirect(url_for('list_recipes'))

# Edit Recipe
@myapp_obj.route('/edit_recipe/<int:recipe_id>', methods=['POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.title = request.form['title']
    recipe.description = request.form['description']
    recipe.ingredients = request.form['ingredients']
    recipe.instructions = request.form['instructions']
    db.session.commit()
    return redirect(url_for('view_recipe', recipe_id=recipe_id))
