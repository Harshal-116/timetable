from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Room, Faculty, Schedule
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
app.config['SECRET_KEY'] = 'pro-secret-key-2025'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Security Decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Admin access required!", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    rooms = Room.query.all()
    slots = ["07:15 - 08:15", "08:15 - 09:15", "09:25 - 10:25", "10:25 - 11:25", "11:35 - 12:35", "12:35 - 01:35", "01:55 - 02:55"]
    schedule = Schedule.query.all()
    return render_template('timetable.html', rooms=rooms, slots=slots, schedule=schedule)

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin_panel():
    if request.method == 'POST':
        slot = request.form.get('slot')
        room_id = request.form.get('room')
        faculty_id = request.form.get('faculty')
        
        # Conflict Checking Logic
        room_busy = Schedule.query.filter_by(time_slot=slot, room_id=room_id).first()
        faculty_busy = Schedule.query.filter_by(time_slot=slot, faculty_id=faculty_id).first()
        
        if room_busy:
            flash(f"Room is already occupied by {room_busy.subject}!", "danger")
        elif faculty_busy:
            flash(f"Faculty member is already teaching {faculty_busy.subject} in another room!", "danger")
        else:
            new_entry = Schedule(
                subject=request.form.get('subject'),
                time_slot=slot,
                room_id=room_id,
                faculty_id=faculty_id,
                color=request.form.get('color')
            )
            db.session.add(new_entry)
            db.session.commit()
            flash("Schedule updated successfully!", "success")
            
    return render_template('admin.html', rooms=Room.query.all(), faculties=Faculty.query.all())

@app.route('/delete/<int:id>')
@admin_required
def delete_entry(id):
    entry = Schedule.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry removed.", "success")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('index'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)