"""
Smart Student Analyzer - Initial Seed Data Generator
Populates realistic demo users, subjects, students, marks, and notifications
as outlined in the Project Synopsis & Data Dictionary.
"""

from database import init_db, query_db, execute_db
from models import create_user, create_student, create_subject, save_or_update_mark, add_notification

def seed_all():
    print("[Seed] Initializing Database Tables...")
    init_db()

    # 1. Check if already seeded
    existing_user = query_db("SELECT * FROM users WHERE username = 'admin'", one=True)
    if existing_user:
        print("[Seed] Database already has admin user. Skipping seed.")
        return

    print("[Seed] Creating administrative and instructor users...")
    create_user('admin', 'admin@smartanalyzer.edu', 'admin123', role='admin')
    create_user('teacher', 'faculty@smartanalyzer.edu', 'teacher123', role='teacher')
    create_user('student', 'student@smartanalyzer.edu', 'student123', role='student')

    print("[Seed] Creating curriculum subjects...")
    subjects = [
        ('CS401', 'Data Structures & Algorithms', 4, 'B.Tech (CS)', 4),
        ('CS402', 'Database Management Systems', 4, 'B.Tech (CS)', 4),
        ('CS403', 'Web Programming with Python Flask', 3, 'B.Tech (CS)', 4),
        ('CS404', 'Software Engineering Principles', 3, 'B.Tech (CS)', 4),
        ('CS405', 'Computer Networks & Security', 3, 'B.Tech (CS)', 4),
        ('BCA301', 'Object Oriented Programming', 4, 'BCA', 3),
        ('BCA302', 'Operating Systems', 3, 'BCA', 3),
        ('BCA303', 'Discrete Mathematics', 4, 'BCA', 3),
    ]
    for sub in subjects:
        create_subject(*sub)

    print("[Seed] Creating student master profiles...")
    students = [
        ('CS10123', 'Rohit', 'Sharma', 'B.Tech (CS)', 4, '2004-04-12', 'Male', '9876543210', 'rohit.sharma@college.edu'),
        ('CS10124', 'Priya', 'Patel', 'B.Tech (CS)', 4, '2004-08-23', 'Female', '9876543211', 'priya.patel@college.edu'),
        ('CS10125', 'Rahul', 'Verma', 'B.Tech (CS)', 4, '2003-11-05', 'Male', '9876543212', 'rahul.verma@college.edu'),
        ('CS10126', 'Ananya', 'Singh', 'B.Tech (CS)', 4, '2004-01-19', 'Female', '9876543213', 'ananya.singh@college.edu'),
        ('CS10127', 'Amit', 'Kumar', 'B.Tech (CS)', 4, '2003-09-14', 'Male', '9876543214', 'amit.kumar@college.edu'),
        ('CS10128', 'Vikram', 'Joshi', 'B.Tech (CS)', 4, '2004-03-30', 'Male', '9876543215', 'vikram.joshi@college.edu'),
        ('CS10129', 'Sneha', 'Gupta', 'B.Tech (CS)', 4, '2004-06-11', 'Female', '9876543216', 'sneha.gupta@college.edu'),
        ('CS10130', 'Manish', 'Tiwari', 'B.Tech (CS)', 4, '2003-12-01', 'Male', '9876543217', 'manish.tiwari@college.edu'),
        ('BCA2001', 'Neha', 'Sharma', 'BCA', 3, '2005-02-14', 'Female', '9876543218', 'neha.sharma@college.edu'),
        ('BCA2002', 'Rajesh', 'Nair', 'BCA', 3, '2004-10-25', 'Male', '9876543219', 'rajesh.nair@college.edu'),
    ]
    for st in students:
        create_student(*st)

    print("[Seed] Populating academic examination marks...")
    # Fetch DB IDs
    db_students = {s['roll_no']: s['student_id'] for s in query_db("SELECT roll_no, student_id FROM students")}
    db_subjects = {s['subject_code']: s['subject_id'] for s in query_db("SELECT subject_code, subject_id FROM subjects")}

    # Define marks distributions
    # (Roll, Subject Code, Marks Obtained, Max Marks)
    sample_marks = [
        # Rohit Sharma - Outstanding (avg ~91%)
        ('CS10123', 'CS401', 94.0, 100.0),
        ('CS10123', 'CS402', 89.0, 100.0),
        ('CS10123', 'CS403', 95.0, 100.0),
        ('CS10123', 'CS404', 90.0, 100.0),
        ('CS10123', 'CS405', 88.0, 100.0),

        # Priya Patel - Excellent (avg ~86%)
        ('CS10124', 'CS401', 88.0, 100.0),
        ('CS10124', 'CS402', 82.0, 100.0),
        ('CS10124', 'CS403', 91.0, 100.0),
        ('CS10124', 'CS404', 85.0, 100.0),
        ('CS10124', 'CS405', 84.0, 100.0),

        # Rahul Verma - Very Good (avg ~75%)
        ('CS10125', 'CS401', 72.0, 100.0),
        ('CS10125', 'CS402', 76.0, 100.0),
        ('CS10125', 'CS403', 80.0, 100.0),
        ('CS10125', 'CS404', 74.0, 100.0),
        ('CS10125', 'CS405', 73.0, 100.0),

        # Ananya Singh - Good (avg ~64%)
        ('CS10126', 'CS401', 65.0, 100.0),
        ('CS10126', 'CS402', 61.0, 100.0),
        ('CS10126', 'CS403', 68.0, 100.0),
        ('CS10126', 'CS404', 62.0, 100.0),
        ('CS10126', 'CS405', 64.0, 100.0),

        # Amit Kumar - Pass / Borderline (avg ~53%)
        ('CS10127', 'CS401', 52.0, 100.0),
        ('CS10127', 'CS402', 50.0, 100.0),
        ('CS10127', 'CS403', 58.0, 100.0),
        ('CS10127', 'CS404', 51.0, 100.0),
        ('CS10127', 'CS405', 54.0, 100.0),

        # Vikram Joshi - At Risk / Weak (avg ~42%)
        ('CS10128', 'CS401', 38.0, 100.0),
        ('CS10128', 'CS402', 42.0, 100.0),
        ('CS10128', 'CS403', 45.0, 100.0),
        ('CS10128', 'CS404', 39.0, 100.0),
        ('CS10128', 'CS405', 46.0, 100.0),

        # Sneha Gupta - Outstanding (avg ~93%)
        ('CS10129', 'CS401', 95.0, 100.0),
        ('CS10129', 'CS402', 91.0, 100.0),
        ('CS10129', 'CS403', 96.0, 100.0),
        ('CS10129', 'CS404', 92.0, 100.0),
        ('CS10129', 'CS405', 91.0, 100.0),

        # Manish Tiwari - At Risk (avg ~37%)
        ('CS10130', 'CS401', 34.0, 100.0),
        ('CS10130', 'CS402', 36.0, 100.0),
        ('CS10130', 'CS403', 42.0, 100.0),
        ('CS10130', 'CS404', 35.0, 100.0),
        ('CS10130', 'CS405', 38.0, 100.0),

        # BCA Students
        ('BCA2001', 'BCA301', 82.0, 100.0),
        ('BCA2001', 'BCA302', 78.0, 100.0),
        ('BCA2001', 'BCA303', 85.0, 100.0),

        ('BCA2002', 'BCA301', 65.0, 100.0),
        ('BCA2002', 'BCA302', 68.0, 100.0),
        ('BCA2002', 'BCA303', 62.0, 100.0),
    ]

    for roll, sub_code, marks_ob, max_m in sample_marks:
        st_id = db_students.get(roll)
        sub_id = db_subjects.get(sub_code)
        if st_id and sub_id:
            save_or_update_mark(st_id, sub_id, marks_ob, max_m, 'Semester Exam')

    print("[Seed] Adding system notifications...")
    add_notification("System initialized with semester performance data.", n_type='info')
    add_notification("Academic Alert: Student Vikram Joshi (CS10128) identified as At-Risk (<50%).", n_type='warning')
    add_notification("Academic Alert: Student Manish Tiwari (CS10130) identified as At-Risk (<50%).", n_type='danger')
    add_notification("Top Performer Award: Sneha Gupta (CS10129) achieved 93% with Grade A+.", n_type='success')

    print("[Seed] Seed data successfully populated!")

if __name__ == '__main__':
    seed_all()
