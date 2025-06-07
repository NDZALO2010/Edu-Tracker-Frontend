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

lecturers_data = {
    'lecturer1': {
        'lecturer_number': 'from database',
        'surname_initials': 'from database',
        'email': 'from database',
        'cellphone': 'from database',
        'modules': [
            {'code': 'CS101', 'name': 'Computer Science 101'},
            {'code': 'MA101', 'name': 'Mathematics 101'}
        ]
    }
}

attendance_records = []  # To store attendance records
feedback_records = []    # To store feedback submissions

# New global list to store class schedules
class_schedules = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            # Determine role automatically
            if username in students_data:
                role = 'student'
            elif username in lecturers_data:
                role = 'lecturer'
            else:
                error = "Invalid username or password"
                return render_template('login.html', error=error)
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_number = request.form.get('student_number')
        surname_initials = request.form.get('surname_initials')
        email = request.form.get('email')
        cellphone = request.form.get('cellphone')
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([student_number, surname_initials, email, cellphone, role, username, password]):
            error = "Please fill all fields"
            return render_template('register.html', error=error)
        # Check if username already exists
        if username in students_data or username in lecturers_data:
            error = "Username already exists"
            return render_template('register.html', error=error)
        if role == 'student':
            students_data[username] = {
                'student_number': student_number,
                'surname_initials': surname_initials,
                'email': email,
                'cellphone': cellphone,
                'modules': [
                    {'code': 'CS101', 'name': 'Computer Science 101', 'lecturer': '555666'},
                    {'code': 'MA101', 'name': 'Mathematics 101', 'lecturer': '555666'}
                ]
            }
        elif role == 'lecturer':
            lecturers_data[username] = {
                'lecturer_number': student_number,
                'surname_initials': surname_initials,
                'email': email,
                'cellphone': cellphone,
                'modules': [
                    {'code': 'CS101', 'name': 'Computer Science 101'},
                    {'code': 'MA101', 'name': 'Mathematics 101'}
                ]
            }
        else:
            error = "Invalid role selected"
            return render_template('register.html', error=error)
        return redirect(url_for('login'))
    return render_template('register.html')

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
        if 'class_name' in request.form and 'class_date' in request.form and 'start_time' in request.form and 'end_time' in request.form:
            module_code = request.form.get('module')
            class_name = request.form.get('class_name')
            class_date = request.form.get('class_date')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            if module_code and class_name and class_date and start_time and end_time:
                from datetime import datetime
                # Compute day of the week from class_date
                try:
                    day = datetime.strptime(class_date, "%Y-%m-%d").strftime("%A")
                except ValueError:
                    day = ""
                # Add new class schedule
                class_schedules.append({
                    'lecturer': username,
                    'module_code': module_code,
                    'class_name': class_name,
                    'day': day,
                    'date': class_date,
                    'start_time': start_time,
                    'end_time': end_time
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

    lecturer_info = lecturers_data.get(username, {})

    return render_template('dashboard_lecturer.html', username=username, modules=lecturer_modules, attendance=filtered_attendance, selected_module=selected_module_code, class_schedules=lecturer_schedules, lecturer_info=lecturer_info)


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

    student_info = students_data.get(username, {})

    return render_template('dashboard_student.html', username=username, student=student, attendance=attendance_records, class_schedules=student_schedules, student_info=student_info)

# Removed admin dashboard route and admin role references as per request

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

import csv
from io import StringIO
from flask import Response

@app.route('/download_class_schedule')
@role_required(['lecturer'])
def download_class_schedule():
    username = session.get('username')
    lecturer_schedules = [cs for cs in class_schedules if cs['lecturer'] == username]

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Module Code', 'Class Name', 'Day', 'Date', 'Start Time', 'End Time'])
    for cs in lecturer_schedules:
        cw.writerow([cs['module_code'], cs['class_name'], cs['day'], cs['date'], cs['start_time'], cs['end_time']])
    output = si.getvalue()
    si.close()

    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=class_schedule.csv'}
    )

@app.route('/download_attendance_records')
@role_required(['lecturer'])
def download_attendance_records():
    username = session.get('username')
    module_code = request.args.get('module')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    filtered_attendance = [record for record in attendance_records if record['module'] == module_code]

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
            pass

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Student Number', 'Class Name', 'Date', 'Time', 'Status'])
    for record in filtered_attendance:
        cw.writerow([record['student'], record['class_name'], record['date'], record['time'], record['status']])
    output = si.getvalue()
    si.close()

    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=attendance_records.csv'}
    )

if __name__ == '__main__':
    app.run(debug=True)
