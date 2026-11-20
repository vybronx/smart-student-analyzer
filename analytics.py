"""
Smart Student Analyzer - Performance Analytics Engine
Module 7.4 implementation as specified in Project Synopsis:
Calculates percentages, assigns grades, tracks semester progression,
evaluates subject-wise performance, and flags at-risk students.
"""

def calculate_grade(percentage):
    """Assigns academic letter grade based on percentage."""
    if percentage >= 90.0:
        return 'A+', 'Outstanding'
    elif percentage >= 80.0:
        return 'A', 'Excellent'
    elif percentage >= 70.0:
        return 'B', 'Very Good'
    elif percentage >= 60.0:
        return 'C', 'Good'
    elif percentage >= 50.0:
        return 'D', 'Pass'
    else:
        return 'F', 'Fail / Needs Attention'

def compute_student_summary(marks_records):
    """
    Computes overall percentage, grade, performance status, 
    and subject breakdown for a list of mark records.
    Formula: Percentage = (Σ Marks Obtained / Σ Total Marks) * 100
    """
    if not marks_records:
        return {
            'total_obtained': 0.0,
            'total_max': 0.0,
            'percentage': 0.0,
            'grade': 'N/A',
            'status': 'No Records',
            'passed_subjects': 0,
            'failed_subjects': 0,
            'total_subjects': 0,
            'is_at_risk': False
        }
    
    total_obtained = sum(float(r['marks_obtained']) for r in marks_records)
    total_max = sum(float(r['max_marks']) for r in marks_records)
    
    percentage = round((total_obtained / total_max) * 100.0, 2) if total_max > 0 else 0.0
    grade, status = calculate_grade(percentage)
    
    failed_count = sum(1 for r in marks_records if float(r['marks_obtained']) < (float(r['max_marks']) * 0.40))
    passed_count = len(marks_records) - failed_count
    
    # At risk if overall percentage < 50% or failed any subject
    is_at_risk = percentage < 50.0 or failed_count > 0
    
    return {
        'total_obtained': round(total_obtained, 2),
        'total_max': round(total_max, 2),
        'percentage': percentage,
        'grade': grade,
        'status': status,
        'passed_subjects': passed_count,
        'failed_subjects': failed_count,
        'total_subjects': len(marks_records),
        'is_at_risk': is_at_risk
    }

def analyze_subject_trends(subject_marks_list):
    """
    Computes statistics for a given subject across all students:
    Average, Highest, Lowest, Total Students, Pass Rate.
    """
    if not subject_marks_list:
        return {
            'avg_marks': 0.0,
            'highest_marks': 0.0,
            'lowest_marks': 0.0,
            'count': 0,
            'pass_percentage': 0.0
        }
    
    scores = [float(item['marks_obtained']) for item in subject_marks_list]
    max_scores = [float(item['max_marks']) for item in subject_marks_list]
    
    avg_score = round(sum(scores) / len(scores), 2)
    highest_score = round(max(scores), 2)
    lowest_score = round(min(scores), 2)
    
    passing = sum(1 for s, m in zip(scores, max_scores) if s >= (m * 0.40))
    pass_pct = round((passing / len(scores)) * 100.0, 2)
    
    return {
        'avg_marks': avg_score,
        'highest_marks': highest_score,
        'lowest_marks': lowest_score,
        'count': len(scores),
        'pass_percentage': pass_pct
    }

def analyze_grade_distribution(student_summaries):
    """
    Generates counts for A+, A, B, C, D, F for charts.
    """
    distribution = {'A+': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for summary in student_summaries:
        g = summary.get('grade')
        if g in distribution:
            distribution[g] += 1
    return distribution
