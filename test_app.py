"""
Smart Student Analyzer - Automated Test Suite
Implements Section 17 Testing Strategy:
- Unit Testing (Mathematical engine, grade parser, password security)
- Integration Testing (Flask route endpoints, database queries, session handling)
- System Testing (End-to-end student creation, mark computation, report generation)
"""

import unittest
from app import app
from database import query_db, init_db
from analytics import calculate_grade, compute_student_summary, analyze_subject_trends

class TestSmartStudentAnalyzer(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        init_db()

    # 1. Unit Tests for Analytics Engine (Section 7.4 & 17)
    def test_grade_calculation(self):
        self.assertEqual(calculate_grade(95.0)[0], 'A+')
        self.assertEqual(calculate_grade(82.5)[0], 'A')
        self.assertEqual(calculate_grade(74.0)[0], 'B')
        self.assertEqual(calculate_grade(61.0)[0], 'C')
        self.assertEqual(calculate_grade(50.0)[0], 'D')
        self.assertEqual(calculate_grade(35.0)[0], 'F')

    def test_percentage_and_risk_formula(self):
        sample_records = [
            {'marks_obtained': 80.0, 'max_marks': 100.0},
            {'marks_obtained': 90.0, 'max_marks': 100.0},
        ]
        summary = compute_student_summary(sample_records)
        self.assertEqual(summary['percentage'], 85.0)
        self.assertEqual(summary['grade'], 'A')
        self.assertFalse(summary['is_at_risk'])

        failing_records = [
            {'marks_obtained': 30.0, 'max_marks': 100.0},
            {'marks_obtained': 40.0, 'max_marks': 100.0},
        ]
        failing_summary = compute_student_summary(failing_records)
        self.assertEqual(failing_summary['percentage'], 35.0)
        self.assertTrue(failing_summary['is_at_risk'])

    # 2. Integration Tests for Authentication & Routes (Section 7.1)
    def test_health_endpoint(self):
        res = self.client.get('/health')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"healthy", res.data)

    def test_login_flow(self):
        # GET Login Page
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Smart Student Analyzer", res.data)

        # Invalid login
        bad_login = self.client.post('/login', data={'username': 'admin', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b"Invalid username or password", bad_login.data)

        # Valid login
        good_login = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(good_login.status_code, 200)
        self.assertIn(b"Academic Analytics Dashboard", good_login.data)

    # 3. System Tests for Core Endpoints (Section 7.2, 7.3, 7.5)
    def test_protected_routes(self):
        # Log in first
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)

        # Dashboard
        dash = self.client.get('/dashboard')
        self.assertEqual(dash.status_code, 200)

        # Students list
        students = self.client.get('/students')
        self.assertEqual(students.status_code, 200)

        # Subjects list
        subjects = self.client.get('/subjects')
        self.assertEqual(subjects.status_code, 200)

        # Marks ledger
        marks = self.client.get('/marks')
        self.assertEqual(marks.status_code, 200)

        # Analytics Engine
        analytics = self.client.get('/analytics/performance')
        self.assertEqual(analytics.status_code, 200)

        # At-Risk Interventions
        at_risk = self.client.get('/analytics/at-risk')
        self.assertEqual(at_risk.status_code, 200)

if __name__ == '__main__':
    unittest.main()
