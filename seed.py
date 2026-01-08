from app import app
from models import db, User, Room, Faculty

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Add Users
        admin = User(username='admin', password='123', role='admin')
        faculty_user = User(username='faculty', password='123', role='faculty')
        db.session.add_all([admin, faculty_user])
        
        # Add Rooms from your image
        rooms = [Room(name=n) for n in ['208', '209', '401', '409', 'Main Lab', 'DS Lab']]
        db.session.add_all(rooms)
        
        # Add Faculty from your image
        faculty_names = ['Vandana', 'Zunaira', 'Omkar', 'Saba', 'Esmita', 'Rajeshwari']
        faculties = [Faculty(name=n) for n in faculty_names]
        db.session.add_all(faculties)
        
        db.session.commit()
        print("Database Seeded Successfully!")

if __name__ == '__main__':
    seed()