from database import query_db, execute_db
from werkzeug.security import generate_password_hash, check_password_hash
from analytics import compute_student_summary, calculate_grade, analyze_subject_trends, analyze_grade_distribution

# ----------------- USER AUTHENTICATION -----------------

def get_user_by_username(username):
    return query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)

def get_user_by_id(user_id):
    return query_db("SELECT * FROM users WHERE user_id = %s", (user_id,), one=True)

def create_user(username, email, password, role='teacher'):
    hashed_pwd = generate_password_hash(password)
    return execute_db(
        "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
        (username, email, hashed_pwd, role)
    )

def verify_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None

# ----------------- STUDENT MANAGEMENT -----------------

def get_all_students(search_query=None, course=None, semester=None):
    sql = "SELECT * FROM students WHERE 1=1"
    params = []
    
    if search_query:
        sql += " AND (first_name LIKE %s OR last_name LIKE %s OR roll_no LIKE %s)"
        like_val = f"%{search_query}%"
        params.extend([like_val, like_val, like_val])
    
    if course:
        sql += " AND course = %s"
        params.append(course)
        
    if semester:
        sql += " AND semester = %s"
        params.append(semester)
        
    sql += " ORDER BY roll_no ASC"
    return query_db(sql, tuple(params))

def get_student_by_id(student_id):
    return query_db("SELECT * FROM students WHERE student_id = %s", (student_id,), one=True)

def get_student_by_roll(roll_no):
    return query_db("SELECT * FROM students WHERE roll_no = %s", (roll_no,), one=True)

def create_student(roll_no, first_name, last_name, course, semester, dob=None, gender='Male', contact_number=None, email=None, user_id=None):
    return execute_db(
        """INSERT INTO students (roll_no, first_name, last_name, course, semester, dob, gender, contact_number, email, user_id)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (roll_no, first_name, last_name, course, semester, dob, gender, contact_number, email, user_id)
    )

def update_student(student_id, roll_no, first_name, last_name, course, semester, dob=None, gender='Male', contact_number=None, email=None):
    execute_db(
        """UPDATE students SET roll_no = %s, first_name = %s, last_name = %s, 
           course = %s, semester = %s, dob = %s, gender = %s, contact_number = %s, email = %s
           WHERE student_id = %s""",
        (roll_no, first_name, last_name, course, semester, dob, gender, contact_number, email, student_id)
    )

def delete_student(student_id):
    execute_db("DELETE FROM students WHERE student_id = %s", (student_id,))

# ----------------- SUBJECT MANAGEMENT -----------------

def get_all_subjects(course=None, semester=None):
    sql = "SELECT * FROM subjects WHERE 1=1"
    params = []
    if course:
        sql += " AND course = %s"
        params.append(course)
    if semester:
        sql += " AND semester = %s"
        params.append(semester)
    sql += " ORDER BY semester, subject_code"
    return query_db(sql, tuple(params))

def get_subject_by_id(subject_id):
    return query_db("SELECT * FROM subjects WHERE subject_id = %s", (subject_id,), one=True)

def create_subject(subject_code, subject_name, credits, course, semester):
    return execute_db(
        "INSERT INTO subjects (subject_code, subject_name, credits, course, semester) VALUES (%s, %s, %s, %s, %s)",
        (subject_code, subject_name, credits, course, semester)
    )

def update_subject(subject_id, subject_code, subject_name, credits, course, semester):
    execute_db(
        "UPDATE subjects SET subject_code = %s, subject_name = %s, credits = %s, course = %s, semester = %s WHERE subject_id = %s",
        (subject_code, subject_name, credits, course, semester, subject_id)
    )

def delete_subject(subject_id):
    execute_db("DELETE FROM subjects WHERE subject_id = %s", (subject_id,))

# ----------------- ACADEMIC MARKS RECORDS -----------------

def get_marks_by_student(student_id):
    sql = """
        SELECT m.*, s.subject_code, s.subject_name, s.credits, s.semester as subject_semester
        FROM marks m
        JOIN subjects s ON m.subject_id = s.subject_id
        WHERE m.student_id = %s
        ORDER BY s.semester, s.subject_code
    """
    return query_db(sql, (student_id,))

def get_all_marks(course=None, semester=None):
    sql = """
        SELECT m.*, st.roll_no, st.first_name, st.last_name, st.course, st.semester as student_semester,
               sub.subject_code, sub.subject_name, sub.credits
        FROM marks m
        JOIN students st ON m.student_id = st.student_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE 1=1
    """
    params = []
    if course:
        sql += " AND st.course = %s"
        params.append(course)
    if semester:
        sql += " AND st.semester = %s"
        params.append(semester)
    sql += " ORDER BY st.roll_no ASC, sub.subject_code ASC"
    return query_db(sql, tuple(params))

def save_or_update_mark(student_id, subject_id, marks_obtained, max_marks=100.0, exam_type='Semester Exam'):
    pct = (float(marks_obtained) / float(max_marks)) * 100.0 if float(max_marks) > 0 else 0.0
    grade, _ = calculate_grade(pct)
    
    existing = query_db(
        "SELECT mark_id FROM marks WHERE student_id = %s AND subject_id = %s AND exam_type = %s",
        (student_id, subject_id, exam_type),
        one=True
    )
    if existing:
        execute_db(
            "UPDATE marks SET marks_obtained = %s, max_marks = %s, grade = %s WHERE mark_id = %s",
            (marks_obtained, max_marks, grade, existing['mark_id'])
        )
        return existing['mark_id']
    else:
        return execute_db(
            "INSERT INTO marks (student_id, subject_id, exam_type, marks_obtained, max_marks, grade) VALUES (%s, %s, %s, %s, %s, %s)",
            (student_id, subject_id, exam_type, marks_obtained, max_marks, grade)
        )

def delete_mark(mark_id):
    execute_db("DELETE FROM marks WHERE mark_id = %s", (mark_id,))

# ----------------- DASHBOARD & ANALYTICS DATA -----------------

def get_dashboard_summary():
    students = get_all_students()
    subjects = get_all_subjects()
    
    student_summaries = []
    top_performer = None
    max_pct = -1.0
    at_risk_list = []
    
    for student in students:
        marks = get_marks_by_student(student['student_id'])
        summary = compute_student_summary(marks)
        student_data = {**student, **summary}
        student_summaries.append(student_data)
        
        if summary['total_subjects'] > 0:
            if summary['percentage'] > max_pct:
                max_pct = summary['percentage']
                top_performer = student_data
            
            if summary['is_at_risk']:
                at_risk_list.append(student_data)
    
    # Class Average %
    students_with_marks = [s for s in student_summaries if s['total_subjects'] > 0]
    class_avg = round(sum(s['percentage'] for s in students_with_marks) / len(students_with_marks), 2) if students_with_marks else 0.0
    
    # Grade distribution
    grade_distribution = analyze_grade_distribution(student_summaries)
    
    # Subject wise stats
    subject_stats = []
    for sub in subjects:
        sub_marks = query_db("SELECT marks_obtained, max_marks FROM marks WHERE subject_id = %s", (sub['subject_id'],))
        stats = analyze_subject_trends(sub_marks)
        subject_stats.append({
            'code': sub['subject_code'],
            'name': sub['subject_name'],
            'avg_marks': stats['avg_marks'],
            'pass_percentage': stats['pass_percentage'],
            'count': stats['count']
        })
        
    # Semester breakdown
    sem_stats = {}
    for sem in range(1, 9):
        sem_students = [s for s in students_with_marks if s['semester'] == sem]
        if sem_students:
            avg_sem = round(sum(s['percentage'] for s in sem_students) / len(sem_students), 2)
            sem_stats[f"Sem {sem}"] = avg_sem
            
    return {
        'total_students': len(students),
        'total_subjects': len(subjects),
        'class_average': class_avg,
        'top_performer': top_performer,
        'at_risk_count': len(at_risk_list),
        'at_risk_list': at_risk_list,
        'grade_distribution': grade_distribution,
        'subject_stats': subject_stats,
        'sem_stats': sem_stats,
        'students_analyzed': student_summaries
    }

# ----------------- NOTIFICATIONS -----------------

def add_notification(message, n_type='info', user_id=None, student_id=None):
    execute_db(
        "INSERT INTO notifications (message, type, user_id, student_id) VALUES (%s, %s, %s, %s)",
        (message, n_type, user_id, student_id)
    )

def get_recent_notifications(limit=5):
    return query_db("SELECT * FROM notifications ORDER BY created_at DESC LIMIT %s", (limit,))
