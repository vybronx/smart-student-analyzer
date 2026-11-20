import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from database import init_db
from models import (
    verify_user, get_user_by_id,
    get_all_students, get_student_by_id, create_student, update_student, delete_student,
    get_all_subjects, get_subject_by_id, create_subject, update_subject, delete_subject,
    get_marks_by_student, get_all_marks, save_or_update_mark, delete_mark,
    get_dashboard_summary, get_recent_notifications, add_notification,
    compute_student_summary
)

app = Flask(__name__)
app.config.from_object(Config)

# ----------------- AUTHENTICATION DECORATOR -----------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------- ROUTE HANDLERS -----------------

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/health')
def health_check():
    """Lightweight endpoint for UptimeRobot keep-alive monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'Smart Student Analyzer',
        'code': 200
    }), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = verify_user(username, password)
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('login'))

# ----------------- DASHBOARD -----------------

@app.route('/dashboard')
@login_required
def dashboard():
    summary = get_dashboard_summary()
    notifications = get_recent_notifications(limit=5)
    return render_template('dashboard.html', active_page='dashboard', summary=summary, notifications=notifications)

# ----------------- STUDENT MANAGEMENT -----------------

@app.route('/students')
@login_required
def list_students():
    search_query = request.args.get('search', '').strip()
    course = request.args.get('course', '').strip() or None
    semester = request.args.get('semester', '').strip() or None
    
    students = get_all_students(search_query=search_query or None, course=course, semester=semester)
    return render_template(
        'students/list.html',
        active_page='students',
        students=students,
        search_query=search_query,
        selected_course=course,
        selected_sem=semester
    )

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        course = request.form.get('course', '').strip()
        semester = int(request.form.get('semester', 1))
        dob = request.form.get('dob') or None
        gender = request.form.get('gender', 'Male')
        email = request.form.get('email', '').strip() or None
        contact_number = request.form.get('contact_number', '').strip() or None

        try:
            create_student(roll_no, first_name, last_name, course, semester, dob, gender, contact_number, email)
            add_notification(f"New student {first_name} {last_name} ({roll_no}) enrolled.", "info")
            flash("Student profile created successfully!", "success")
            return redirect(url_for('list_students'))
        except Exception as e:
            flash(f"Error adding student: {e}", "danger")

    return render_template('students/add.html', active_page='students')

@app.route('/students/<int:student_id>')
@login_required
def view_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('list_students'))

    marks = get_marks_by_student(student_id)
    summary = compute_student_summary(marks)
    return render_template('students/view.html', active_page='students', student=student, marks=marks, summary=summary)

@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('list_students'))

    if request.method == 'POST':
        roll_no = request.form.get('roll_no', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        course = request.form.get('course', '').strip()
        semester = int(request.form.get('semester', 1))
        dob = request.form.get('dob') or None
        gender = request.form.get('gender', 'Male')
        email = request.form.get('email', '').strip() or None
        contact_number = request.form.get('contact_number', '').strip() or None

        try:
            update_student(student_id, roll_no, first_name, last_name, course, semester, dob, gender, contact_number, email)
            flash("Student profile updated successfully!", "success")
            return redirect(url_for('view_student', student_id=student_id))
        except Exception as e:
            flash(f"Error updating student: {e}", "danger")

    return render_template('students/edit.html', active_page='students', student=student)

@app.route('/students/<int:student_id>/delete', methods=['POST'])
@login_required
def delete_student_route(student_id):
    try:
        delete_student(student_id)
        flash("Student record deleted successfully.", "info")
    except Exception as e:
        flash(f"Error deleting student: {e}", "danger")
    return redirect(url_for('list_students'))

# ----------------- SUBJECT MANAGEMENT -----------------

@app.route('/subjects')
@login_required
def list_subjects():
    course = request.args.get('course', '').strip() or None
    semester = request.args.get('semester', '').strip() or None
    subjects = get_all_subjects(course=course, semester=semester)
    return render_template('subjects/list.html', active_page='subjects', subjects=subjects, selected_course=course, selected_sem=semester)

@app.route('/subjects/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        subject_code = request.form.get('subject_code', '').strip().upper()
        subject_name = request.form.get('subject_name', '').strip()
        credits = int(request.form.get('credits', 3))
        course = request.form.get('course', '').strip()
        semester = int(request.form.get('semester', 1))

        try:
            create_subject(subject_code, subject_name, credits, course, semester)
            flash("Subject added to curriculum successfully!", "success")
            return redirect(url_for('list_subjects'))
        except Exception as e:
            flash(f"Error adding subject: {e}", "danger")

    return render_template('subjects/add.html', active_page='subjects')

@app.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = get_subject_by_id(subject_id)
    if not subject:
        flash("Subject not found.", "danger")
        return redirect(url_for('list_subjects'))

    if request.method == 'POST':
        subject_code = request.form.get('subject_code', '').strip().upper()
        subject_name = request.form.get('subject_name', '').strip()
        credits = int(request.form.get('credits', 3))
        course = request.form.get('course', '').strip()
        semester = int(request.form.get('semester', 1))

        try:
            update_subject(subject_id, subject_code, subject_name, credits, course, semester)
            flash("Subject updated successfully!", "success")
            return redirect(url_for('list_subjects'))
        except Exception as e:
            flash(f"Error updating subject: {e}", "danger")

    return render_template('subjects/edit.html', active_page='subjects', subject=subject)

@app.route('/subjects/<int:subject_id>/delete', methods=['POST'])
@login_required
def delete_subject_route(subject_id):
    try:
        delete_subject(subject_id)
        flash("Subject removed successfully.", "info")
    except Exception as e:
        flash(f"Error deleting subject: {e}", "danger")
    return redirect(url_for('list_subjects'))

# ----------------- MARKS MANAGEMENT -----------------

@app.route('/marks')
@login_required
def list_marks():
    course = request.args.get('course', '').strip() or None
    semester = request.args.get('semester', '').strip() or None
    marks = get_all_marks(course=course, semester=semester)
    return render_template('marks/list.html', active_page='marks', marks=marks, selected_course=course, selected_sem=semester)

@app.route('/marks/add', methods=['GET', 'POST'])
@login_required
def add_mark():
    students = get_all_students()
    subjects = get_all_subjects()
    selected_student_id = request.args.get('student_id', '')

    if request.method == 'POST':
        student_id = int(request.form.get('student_id'))
        subject_id = int(request.form.get('subject_id'))
        exam_type = request.form.get('exam_type', 'Semester Exam')
        marks_obtained = float(request.form.get('marks_obtained', 0))
        max_marks = float(request.form.get('max_marks', 100))

        try:
            save_or_update_mark(student_id, subject_id, marks_obtained, max_marks, exam_type)
            st = get_student_by_id(student_id)
            if marks_obtained < (max_marks * 0.40):
                add_notification(f"Warning: {st['first_name']} {st['last_name']} ({st['roll_no']}) failed in course.", "danger", student_id=student_id)
            flash("Marks entry saved and grade updated!", "success")
            return redirect(url_for('view_student', student_id=student_id))
        except Exception as e:
            flash(f"Error recording marks: {e}", "danger")

    return render_template('marks/add.html', active_page='marks', students=students, subjects=subjects, selected_student_id=selected_student_id)

@app.route('/marks/<int:mark_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_mark(mark_id):
    from database import query_db
    mark = query_db("""
        SELECT m.*, st.roll_no, st.first_name, st.last_name, s.subject_code, s.subject_name
        FROM marks m
        JOIN students st ON m.student_id = st.student_id
        JOIN subjects s ON m.subject_id = s.subject_id
        WHERE m.mark_id = %s
    """, (mark_id,), one=True)

    if not mark:
        flash("Mark record not found.", "danger")
        return redirect(url_for('list_marks'))

    if request.method == 'POST':
        exam_type = request.form.get('exam_type', 'Semester Exam')
        marks_obtained = float(request.form.get('marks_obtained', 0))
        max_marks = float(request.form.get('max_marks', 100))

        try:
            save_or_update_mark(mark['student_id'], mark['subject_id'], marks_obtained, max_marks, exam_type)
            flash("Marks updated successfully!", "success")
            return redirect(url_for('view_student', student_id=mark['student_id']))
        except Exception as e:
            flash(f"Error updating mark: {e}", "danger")

    return render_template('marks/edit.html', active_page='marks', mark=mark)

@app.route('/marks/<int:mark_id>/delete', methods=['POST'])
@login_required
def delete_mark_route(mark_id):
    try:
        delete_mark(mark_id)
        flash("Mark record deleted successfully.", "info")
    except Exception as e:
        flash(f"Error deleting mark: {e}", "danger")
    return redirect(url_for('list_marks'))

# ----------------- ANALYTICS & INSIGHTS -----------------

@app.route('/analytics/performance')
@login_required
def performance_analytics():
    summary = get_dashboard_summary()
    return render_template('analytics/performance.html', active_page='analytics', summary=summary)

@app.route('/analytics/at-risk')
@login_required
def at_risk_students():
    summary = get_dashboard_summary()
    return render_template('analytics/at_risk.html', active_page='at_risk', at_risk_students=summary['at_risk_list'])

# ----------------- REPORTS & TRANSCRIPTS -----------------

@app.route('/reports/student/<int:student_id>')
@login_required
def student_report(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('list_students'))

    marks = get_marks_by_student(student_id)
    summary = compute_student_summary(marks)
    return render_template('reports/student_report.html', active_page='reports', student=student, marks=marks, summary=summary)

@app.route('/reports/class')
@login_required
def class_reports():
    course = request.args.get('course', '').strip() or None
    semester = request.args.get('semester', '').strip() or None

    students = get_all_students(course=course, semester=semester)
    evaluated_students = []
    for st in students:
        marks = get_marks_by_student(st['student_id'])
        summary = compute_student_summary(marks)
        evaluated_students.append({**st, **summary})

    return render_template(
        'reports/class_report.html',
        active_page='reports',
        students=evaluated_students,
        selected_course=course,
        selected_sem=semester
    )

# ----------------- INITIALIZE APP -----------------

try:
    init_db()
except Exception as _e:
    print(f"[Init Warning] Could not auto-initialize DB on start: {_e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
