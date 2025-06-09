# Student Attendance Tracker with Facial Recognition

This project is a web application designed to track student attendance by confirming if a student has attended class through facial scanning. The system provides role-based access for students, lecturers, and previously admins (now removed). Students mark their attendance by scanning their face, and lecturers can view attendance records and manage class schedules.

## Features

- **Facial Scan Attendance:** Students confirm their attendance by submitting a facial scan.
- **Role-Based Access Control:** Different views and permissions for students and lecturers.
- **Student Dashboard:** View scheduled classes and mark attendance with a button next to each scheduled module.
- **Lecturer Dashboard:** 
  - View attendance records filtered by module and date range.
  - Manage class schedules.
  - **Sidebar Navigation:** A sidebar on the left allows lecturers to easily navigate between New Class Schedule, Class Schedule, and View Students Attendance sections.
  - **Download Functionality:** Lecturers can download class schedules and attendance records as CSV files for offline use.
- **Secure Login:** Users log in by selecting their role and providing credentials.
- **Clean and Professional UI:** Styled with school-appropriate colors and layout, including a login page with a logo.

## Technologies Used

- Python with Flask for backend and routing.
- HTML, CSS for frontend templates and styling.
- Session management for user authentication and role control.

## Installation and Running

1. Clone the repository:
   ```
   git clone https://github.com/NDZALO2010/Edu-Tracker-Frontend.git
   ```
2. Navigate to the project directory:
   ```
   cd Edu-Tracker-Frontend/python-frontend-project
   ```
3. Install required Python packages (Flask):
   ```
   pip install flask
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and go to https://ndzalo2010.github.io/Edu-Tracker-Frontend/ to access the application.

## Author

Ndzalo Mathebula

## License

This project is licensed under the MIT License.
