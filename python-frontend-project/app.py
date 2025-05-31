from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key in production

# Decorator for role-based access control
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session:
                return redirect(url_for('login'))
            if session['role'] not in allowed_roles:
                return "Access denied", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')
        # For demo, accept any username/password
        if role and username and password:
            session['role'] = role
            session['username'] = username
            if role == 'student':
                return redirect(url_for('facial_scan'))
            else:
                return redirect(url_for(f'dashboard_{role}'))
        else:
            error = "Please fill all fields"
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/facial_scan', methods=['GET', 'POST'])
@role_required(['student'])
def facial_scan():
    if request.method == 'POST':
        image_data = request.form.get('imageData')
        if image_data:
            # Here you would add real facial scan verification logic
            # For demo, assume success if image data is present
            return redirect(url_for('dashboard_student'))
        else:
            error = "Facial scan failed. Please try again."
            return render_template('facial_scan.html', error=error)
    return render_template('facial_scan.html')

# Simulated data for demo purposes
students_data = {
    'student1': {
        'student_number': 'from database',
        'surname_initials': 'from datadase.',
        'email': 'from database',
        'cellphone': 'from database',
        'modules': [
            {'code': 'CS101', 'name': 'Computer Science 101', 'lecturer': 'from database'},
            {'code': 'MA101', 'name': 'Mathematics 101', 'lecturer': 'from database'}
        ]
    }
}

attendance_records = []  # To store attendance records
feedback_records = []    # To store feedback submissions

# New global list to store class schedules
class_schedules = []

@app.route('/dashboard_lecturer', methods=['GET', 'POST'])
@role_required(['lecturer'])
def dashboard_lecturer():
    username = session.get('username')
    # Use fixed modules list for lecturer dashboard
    lecturer_modules = [
        {'code': 'CS101', 'name': 'Computer Science 101'},
        {'code': 'MA101', 'name': 'Mathematics 101'}
    ]

    selected_module_code = None
    filtered_attendance = []

    if request.method == 'POST':
        # Check if this is a class schedule submission
        if 'class_name' in request.form and 'class_date' in request.form and 'class_time' in request.form:
            module_code = request.form.get('module')
            class_name = request.form.get('class_name')
            class_date = request.form.get('class_date')
            class_time = request.form.get('class_time')
            if module_code and class_name and class_date and class_time:
                # Add new class schedule
                class_schedules.append({
                    'lecturer': username,
                    'module_code': module_code,
                    'class_name': class_name,
                    'date': class_date,
                    'time': class_time
                })
        else:
            selected_module_code = request.form.get('module')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            if selected_module_code:
                filtered_attendance = [record for record in attendance_records if record['module'] == selected_module_code]

                # Filter by date range if both dates are provided
                if start_date and end_date:
                    from datetime import datetime
                    try:
                        start = datetime.strptime(start_date, "%Y-%m-%d").date()
                        end = datetime.strptime(end_date, "%Y-%m-%d").date()
                        filtered_attendance = [
                            record for record in filtered_attendance
                            if start <= datetime.strptime(record['date'], "%Y-%m-%d").date() <= end
                        ]
                    except ValueError:
                        # If date parsing fails, ignore date filtering
                        pass

    # Get class schedules for this lecturer
    lecturer_schedules = [cs for cs in class_schedules if cs['lecturer'] == username]

    return render_template('dashboard_lecturer.html', username=username, modules=lecturer_modules, attendance=filtered_attendance, selected_module=selected_module_code, class_schedules=lecturer_schedules)


@app.route('/dashboard_student', methods=['GET', 'POST'])
@role_required(['student'])
def dashboard_student():
    username = session.get('username')
    # For demo, map any username to 'student1' data for testing
    student = students_data.get(username)
    if not student:
        # Fallback to 'student1' for demo purposes
        student = students_data.get('student1')
        if not student:
            return "Student data not found", 404

    if request.method == 'POST':
        module_code = request.form.get('module')
        if module_code:
            # Mark attendance and auto send to lecturer
            module = next((m for m in student['modules'] if m['code'] == module_code), None)
            from datetime import datetime
            now = datetime.now()
            attendance_records.append({
                'student': username,
                'module': module_code,
                'class_name': module['name'] if module else '',
                'date': now.strftime("%Y-%m-%d"),
                'time': now.strftime("%H:%M:%S"),
                'status': 'present'
            })
            # Auto send feedback to lecturer as attendance marked
            lecturer = module['lecturer'] if module else None
            if lecturer:
                feedback_records.append({'student': username, 'module': module_code, 'lecturer': lecturer, 'feedback': 'Attendance marked'})
        return redirect(url_for('dashboard_student'))

    # Get class schedules relevant to the student
    student_module_codes = {m['code'] for m in student['modules']}
    student_schedules = [cs for cs in class_schedules if cs['module_code'] in student_module_codes]

    return render_template('dashboard_student.html', username=username, student=student, attendance=attendance_records, class_schedules=student_schedules)

# Removed admin dashboard route and admin role references as per request

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
