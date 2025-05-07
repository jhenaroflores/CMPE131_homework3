import app
from app import myapp_obj
from app.models import db

if __name__ == "__main__":
    with myapp_obj.app_context():
        db.create_all()
    
    app.myapp_obj.run(debug=True)
