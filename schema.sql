-- =====================================================================
-- SMART STUDENT ANALYZER
-- Database Schema for MySQL Server (Community Edition)
-- As per Project Synopsis Specification (Section 16 & Data Dictionary)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS smart_student_analyzer;
USE smart_student_analyzer;

-- 1. Table: users (Administrative & Teacher Authorization Profiles)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'student') NOT NULL DEFAULT 'teacher',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Table: students (Master Student Database Profiles)
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    roll_no VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NULL,
    gender ENUM('Male', 'Female', 'Other') DEFAULT 'Male',
    course VARCHAR(50) NOT NULL,
    semester INT NOT NULL,
    contact_number VARCHAR(20) NULL,
    email VARCHAR(100) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_students_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Table: subjects (Curriculum Course Catalog)
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL DEFAULT 3,
    course VARCHAR(50) NOT NULL,
    semester INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Table: marks (Academic Performance Evaluation Entries)
CREATE TABLE IF NOT EXISTS marks (
    mark_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    exam_type VARCHAR(50) NOT NULL DEFAULT 'Semester Exam',
    marks_obtained DECIMAL(5,2) NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    grade VARCHAR(5) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_marks_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_marks_subject FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    CONSTRAINT uq_student_subject_exam UNIQUE (student_id, subject_id, exam_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Table: reports (Audit & Generated Academic Records)
CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    generated_by VARCHAR(50) NOT NULL,
    file_path VARCHAR(255) NULL,
    generated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reports_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Table: notifications (Academic Risk & Progress Alerts)
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    student_id INT NULL,
    message VARCHAR(255) NOT NULL,
    type VARCHAR(30) DEFAULT 'info', -- 'alert', 'warning', 'info', 'success'
    is_read TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
