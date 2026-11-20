# 🎓 SMART STUDENT ANALYZER
### *A Smart Web-Based System for Student Academic Performance Analysis and Institutional Insights*

---

## 👨‍🎓 About The Project

During our college semesters, we observed that our professors and department staff spent countless hours manually maintaining marks in paper registers and Excel spreadsheets. Calculating percentages by hand, assigning letter grades, and identifying students who were failing or needing urgent counseling was not only time-consuming but also prone to calculation errors.

To solve this practical problem, I built the **Smart Student Analyzer** as my final year academic project. 

It is an automated web-based platform where teachers and administrators can manage student records, record examination marks, and instantly view analytics. The system calculates percentages, assigns grades, visualizes subject trends using interactive charts, tracks semester progress, and automatically flags **At-Risk students** so faculty can arrange timely remedial classes and academic counseling.

---

## 💻 System Requirements

*(Specified in accordance with our Project Synopsis - Section 10)*

### 1. Hardware Requirements
| Component | Minimum Specification | Recommended Specification |
|---|---|---|
| **Processor** | Intel Core i3 or equivalent | Intel Core i5 / AMD Ryzen 5 or higher |
| **RAM** | 4 GB | 8 GB DDR4 |
| **Hard Disk** | 20 GB free space | SSD with 20+ GB free space |
| **Display** | 15-inch monitor (1366 x 768) | Full HD (1920 x 1080) |
| **Input Devices** | Standard Keyboard & Mouse | Standard Keyboard & Mouse |

### 2. Software Requirements
* **Operating System:** Windows 10 / Windows 11 (also runs on Linux / macOS)
* **Backend Framework:** Python 3.9+ with Flask
* **Database Engine:** MySQL Server (Community Edition) / Cloud MySQL (TiDB / Aiven) / SQLite (zero-config local development)
* **Frontend Technologies:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
* **WSGI Production Server:** Gunicorn (for cloud deployment)
* **Development IDE:** Visual Studio Code (VS Code)
* **Supported Browsers:** Google Chrome, Microsoft Edge, Mozilla Firefox

---

## 🛠️ Technology Stack & Architecture

I designed this application following the classic **Three-Tier Software Architecture**:

```
[ User Browser (HTML5 / Bootstrap 5 / Chart.js) ]
                      ▲
                      │  HTTP Requests / JSON Responses
                      ▼
       [ Flask Application Server (Python) ]
                      ▲
                      │  SQL Queries (PyMySQL / SQLite3)
                      ▼
   [ Relational Database (MySQL / TiDB / SQLite) ]
```

* **Frontend (Presentation Layer):** Responsive web interface built using **Bootstrap 5** for mobile and desktop compatibility. Data visualizations are rendered dynamically via **Chart.js**. Printable report cards use custom CSS `@media print` styling for clean paper printouts.
* **Backend (Application Layer):** Lightweight and modular **Python Flask** framework. It handles user sessions, route security, and mathematical analytics computations.
* **Database (Storage Layer):** Normalized relational database with foreign key integrity. Contains tables for `users`, `students`, `subjects`, `marks`, `reports`, and `notifications`.

---

## 🚀 Key Modules & Features

### 1. User Authentication & Role Management (Module 7.1)
* Role-based access control supporting **Administrator**, **Teacher / Faculty**, and **Student** logins.
* Passwords are never stored in plain text; they are encrypted using **PBKDF2-SHA256 salted hashing** via `werkzeug.security`.
* Session-based route protection using custom Python decorators (`@login_required`).

### 2. Student Information Management (Module 7.2)
* Complete registration portal for students with Roll Number, First Name, Last Name, Course Stream, Current Semester, Gender, Contact, and Email.
* Real-time search by student name or roll number, with instant course and semester filtering.

### 3. Subject Curriculum Catalog (Module 7.3)
* Add, update, and manage subjects for different academic programs (e.g., B.Tech CS, BCA, MCA).
* Tracks course codes, subject titles, and credit weightages.

### 4. Examination Marks Ledger & Grade Engine (Module 7.4)
* Records marks for Semester Final Exams, Midterms, Internal Assessments, and Practical Labs.
* **Core Calculation Formula:**
  $$\text{Percentage} = \left(\frac{\sum \text{Marks Obtained}}{\sum \text{Total Marks}}\right) \times 100$$
* **Automated Grading Scale:**
  * **A+ (90% - 100%):** Outstanding Performance
  * **A (80% - 89%):** Excellent
  * **B (70% - 79%):** Very Good
  * **C (60% - 69%):** Good
  * **D (50% - 59%):** Pass / Average
  * **F (Below 50%):** Fail / Academic Alert

### 5. Early Risk Detection (At-Risk Intervention Tracker)
* Identifies students scoring below 50% overall or failing in individual subjects (<40% passing marks).
* Highlights them on a dedicated faculty dashboard so teachers can assign remedial sessions or inform guardians before semester finals.

### 6. Interactive Visual Analytics & Reports (Module 7.5)
* **Dashboard Widgets:** Total enrolled students, overall batch average, current top ranker, and at-risk count.
* **Visual Charts:**
  1. *Subject-Wise Performance:* Bar chart comparing average scores across all subjects.
  2. *Grade Demographics:* Doughnut chart showing distribution of letter grades.
  3. *Semester Progression:* Line chart plotting aggregate trends across semesters.
* **Official Printable Report Card:** Clean, university-standard grade sheet formatted with student bio, tabular marks breakdown, credit summary, and signature lines.
* **Class Consolidated Sheet:** Batch-wide ledger exportable for department meetings.

---

## 📁 Project Directory Structure

```
smart-student-analyzer/
│
├── app.py                     # Main Flask application and URL routing
├── config.py                  # Database connection and environment config
├── database.py                # Database connector (supports MySQL and SQLite)
├── models.py                  # SQL queries and business logic operations
├── analytics.py               # Calculation algorithms (percentages, grades, statistics)
├── schema.sql                 # Official MySQL DDL schema script
├── seed_data.py               # Pre-populated realistic sample data script
├── test_app.py                # Automated unit and integration test suite
├── requirements.txt           # Python package requirements
├── Procfile                   # Process file for cloud hosting (Render)
├── render.yaml                # Render web service configuration
├── run.bat                    # Windows 1-click startup batch script
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file for clean commits
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling, badges, and print CSS
│   └── js/
│       └── main.js            # UI confirmations, tooltips, and print actions
│
└── templates/
    ├── base.html              # Main layout template with sidebar navigation
    ├── login.html             # Secure login screen
    ├── dashboard.html         # Interactive dashboard with Chart.js charts
    ├── students/              # Add, edit, list, and view student profile templates
    ├── subjects/              # Add, edit, and list curriculum subject templates
    ├── marks/                 # Record, edit, and list examination marks templates
    ├── analytics/             # Performance breakdown and At-Risk student templates
    └── reports/               # Printable individual report card & class sheet templates
```

---

## 🏃‍♂️ How to Run Locally on Your Computer

### Prerequisites
Make sure **Python 3.9 or higher** is installed on your system.

### Step 1: Open the Project
Open terminal or PowerShell inside the project directory:
```bash
cd smart-student-analyzer
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Seed Sample Student Data *(Optional but Recommended)*
To populate realistic student records, subjects, marks, and notifications:
```bash
python seed_data.py
```

### Step 4: Start the Server
* **On Windows:** Simply double-click `run.bat` or run:
  ```bash
  python app.py
  ```
* Open your browser and go to:
  👉 **`http://127.0.0.1:5000`**

---

## 🔑 Default Login Credentials

| Role | Username | Password | Permissions |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full administrative control, user & marks management |
| **Faculty / Teacher** | `teacher` | `teacher123` | Enter marks, update students, generate reports |
| **Student** | `student` | `student123` | Read-only view for marks & report cards |

---

## 🌐 Cloud Hosting & 24/7 Keep-Alive Architecture

This project is configured to run on free-tier cloud infrastructure with zero ongoing cost:

1. **Host on Render (Web Service):**
   - Connected directly to our GitHub repository.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
2. **24/7 Uptime with UptimeRobot:**
   - Render's free tier sleeps after 15 minutes of inactivity.
   - We implemented a lightweight `/health` endpoint in `app.py`.
   - An **UptimeRobot HTTP monitor** pings `https://<our-app-url>.onrender.com/health` every 5 minutes, preventing cold-starts and keeping the site instantly accessible 24/7.
3. **Database Persistence:**
   - Works seamlessly with **TiDB Cloud Serverless** or **Aiven MySQL** (Free Forever MySQL wire-compatible databases) via the `DATABASE_URL` environment variable.

---

## 🧪 Testing & Verification

The project includes an automated test suite verifying unit calculations, grade thresholds, authentication workflows, and API endpoints:
```bash
python test_app.py
```
*Verification Result: 5/5 tests passed successfully with 100% endpoint health.*

---

## 📚 Acknowledgments & References

* **Course Textbooks:** IGNOU Software Engineering (BCS-051), Web Programming (BCS-053), Relational Database Design (MCS-014).
* **Framework Documentation:** Python Flask Official Documentation, Bootstrap 5 Docs, Chart.js Guidelines.
* **Faculty Guide:** Department of Computer Science & Engineering.

---

<p align="center">
  <b>Smart Student Analyzer</b> • Developed as a Computer Science Capstone Project • 2026
</p>
