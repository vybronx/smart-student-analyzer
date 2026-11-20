# SMART STUDENT ANALYZER
> **A Web-Based Academic Performance Analysis and Institutional Insights System**

---

## 📌 Abstract & Overview

**Smart Student Analyzer** is a web-based student performance management and analytics application designed to replace cumbersome manual record-keeping and standalone spreadsheets. Developed using **Python Flask**, **MySQL**, and **Bootstrap 5**, the platform offers a centralized database for managing student profiles, registering curriculum subjects, recording examination marks, calculating percentage metrics, and generating letter grades automatically.

The system incorporates early-risk identification algorithms that actively flag academically weak students for counseling, as well as an analytics engine that displays subject averages, grade distributions, and semester progress graphs.

---

## ⚙️ System Requirements

### 1. Hardware Requirements
* **Processor:** Intel Core i3 / i5 or equivalent (2.0 GHz+)
* **RAM:** 4 GB minimum (8 GB recommended)
* **Storage:** 20 GB free space
* **Display:** 1366x768 resolution or higher

### 2. Software Requirements
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5 Framework, Chart.js
* **Backend:** Python 3.9+ with Flask Web Framework
* **WSGI Production Server:** Gunicorn
* **Database:** MySQL Server (Community Edition) / TiDB Cloud / SQLite (Local fallback)
* **Browser:** Google Chrome, Microsoft Edge, Mozilla Firefox

---

## 🏗️ System Architecture & Core Modules

The application is built on a standard **Three-Tier Architecture**:
1. **Presentation Layer (Frontend):** Responsive Bootstrap 5 interface, interactive Chart.js graphs, printable report cards.
2. **Application Layer (Backend Logic):** Python Flask handling role-based authentication, request routing, and data processing.
3. **Database Layer:** Relational database (`schema.sql`) maintaining students, subjects, marks, and audit reports.

### Functional Modules:
1. **User Authentication Module:** Secure role-based login (`admin`, `teacher`, `student`) with salted password hashing (`PBKDF2-SHA256`).
2. **Student Information Management Module:** Full CRUD operations for student records, enrollment indexing, search and semester filtering.
3. **Curriculum & Marks Management Module:** Subject course registry, credits allocation, examination entry (Semester Finals, Midterms, Practicals).
4. **Performance Analytics Engine:**
   * Formula:
     $$\text{Percentage} = \left(\frac{\sum \text{Marks Obtained}}{\sum \text{Total Marks}}\right) \times 100$$
   * Automated Grade Scale:
     * **A+** ($\ge 90\%$): Outstanding
     * **A** ($80\% - 89\%$): Excellent
     * **B** ($70\% - 79\%$): Very Good
     * **C** ($60\% - 69\%$): Good
     * **D** ($50\% - 59\%$): Pass / Average
     * **F** ($< 50\%$): Fail / Needs Intervention
5. **Early Academic Intervention (At-Risk Tracker):** Automatically detects students with aggregate scores below 50% or failed subjects to enable remedial coaching.
6. **Reporting & Visual Dashboard:**
   * Executive summary metrics (Total Enrolled, Class Average, Top Performer, At-Risk Count).
   * Interactive charts (Subject averages, Grade demographic doughnut, Semester progression line chart).
   * Printable University-standard individual student transcripts and semester batch reports.

---

## 📂 Project Directory Structure

```
Smart_Student_Analyzer/
├── app.py                     # Main Flask web application and API endpoints
├── config.py                  # Database & application environment configuration
├── database.py                # Database connection manager (MySQL & SQLite fallback)
├── models.py                  # Database query helper functions & CRUD logic
├── analytics.py               # Performance Analytics mathematical engine
├── schema.sql                 # MySQL schema script
├── seed_data.py               # Pre-populated demo database generator
├── test_app.py                # Automated unit and integration test suite
├── requirements.txt           # Python application dependencies
├── Procfile                   # Gunicorn process file for Render deployment
├── render.yaml                # Render service definition file
├── run.bat                    # One-click Windows startup batch script
├── .env.example               # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css          # Custom layout styles & print media stylesheets
│   └── js/
│       └── main.js            # Frontend interactivity and confirmations
└── templates/
    ├── base.html              # Layout master template with sidebar navigation
    ├── login.html             # Secure user authentication portal
    ├── dashboard.html         # Interactive analytics dashboard with Chart.js
    ├── students/              # Student directory, registration, edit & view views
    ├── subjects/              # Course curriculum catalog and management views
    ├── marks/                 # Academic examination marks ledger views
    ├── analytics/             # Performance trends & At-Risk intervention tracker
    └── reports/               # Printable individual report cards & batch summaries
```

---

## 💻 Local Setup & Execution Guide

### Step 1: Clone or Open Project
Open the project directory in your terminal or IDE (VS Code).

### Step 2: Install Required Libraries
```bash
pip install -r requirements.txt
```

### Step 3: Populate Initial Demo Data
```bash
python seed_data.py
```

### Step 4: Run the Web Server
**Option A (Windows 1-Click):**
Double-click `run.bat`

**Option B (Command Line):**
```bash
python app.py
```

Access the application in your browser at:
👉 **`http://127.0.0.1:5000`**

### Default Sign-In Credentials:
* **Administrator:** Username: `admin` | Password: `admin123`
* **Faculty / Teacher:** Username: `teacher` | Password: `teacher123`
* **Student:** Username: `student` | Password: `student123`

---

## 🌐 Free Cloud Hosting Guide (Render + Free MySQL + UptimeRobot)

### 1. Free Cloud MySQL Setup (TiDB Cloud Serverless)
1. Sign up for a free account at [TiDB Cloud](https://tidbcloud.com/) (No credit card required, 5 GB free forever).
2. Create a free **Serverless Cluster**.
3. Under **Connection**, select **General Connection String** (format: `mysql://<user>:<password>@<host>:4000/<database>`).
4. Copy the connection string.

### 2. Render Deployment
1. Push your repository to GitHub or GitLab.
2. Sign in to [Render](https://render.com/) and click **New +** -> **Web Service**.
3. Connect your repository.
4. Configure service settings:
   * **Runtime:** Python 3
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`
   * **Instance Type:** Free
5. Under **Environment Variables**, add:
   * `DATABASE_URL`: *(Your TiDB Cloud / MySQL connection string)*
   * `SECRET_KEY`: *(A random secure string)*
6. Click **Deploy Web Service**. Render will build and deploy the app!

### 3. Keep-Alive Configuration (UptimeRobot)
Render's free tier spins down if no request is received for 15 minutes. To keep it active 24/7:
1. Sign up for free at [UptimeRobot](https://uptimerobot.com/).
2. Click **Add New Monitor**.
3. **Monitor Type:** `HTTP(s)`
4. **Friendly Name:** `Smart Student Analyzer`
5. **URL:** `https://your-app-name.onrender.com/health`
6. **Monitoring Interval:** `5 minutes`
7. Click **Create Monitor**.
*UptimeRobot will send a heartbeat ping every 5 minutes to keep the Render server active around the clock.*

---

## 🧪 Verification & Automated Testing

The project includes an automated test suite verifying calculation logic, grade assignments, risk thresholds, authentication, and API endpoints:

```bash
python test_app.py
```
*Result: 5/5 passed with 100% endpoint availability.*

---

## 👨‍💻 Project Authors & Academic Submission
* **Project Name:** Smart Student Analyzer
* **Course:** Bachelor of Computer Applications / B.Tech Computer Science
* **Academic Year:** 2026
