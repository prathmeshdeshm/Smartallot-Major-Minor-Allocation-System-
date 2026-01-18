# SmartAllot: Smart Minor & OE Allocation System

This document provides step-by-step instructions on how to set up and run the SmartAllot project locally for development and testing.

## Project Structure

```
Smartallot-Major-Minor-Allocation-System-/
├── smartallot/                 # Main Django project directory
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
├── allotment/                 # Django app for allotment functionality
│   ├── __init__.py
│   ├── admin.py               # Admin configuration
│   ├── apps.py                # App configuration
│   ├── forms.py               # Django forms
│   ├── models.py              # Database models
│   ├── tests.py               # Unit tests
│   ├── urls.py                # App URL patterns
│   ├── utils.py               # Utility functions
│   └── views.py               # View functions
├── templates/                 # HTML templates
│   └── allotment/
│       ├── home.html
│       ├── admin_dashboard.html
│       ├── student_dashboard.html
│       ├── manage_courses.html
│       ├── course_form.html
│       ├── rule_form.html
│       ├── oe_rule_form.html
│       └── confirm_delete.html
├── static/                    # Static files (CSS, JS, images)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in git)
├── build.sh                   # Build script for deployment
└── README.md                  # This file
```

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.9+**
- **PostgreSQL**: A running instance of PostgreSQL.
- **Redis**: A running instance of Redis.
- **Git**

---

## 1. Project Setup

### a. Clone the Repository
Clone the project to your local machine:
```bash
git clone <your-repository-url>
cd Smartallot-Major-Minor-Allocation-System-
```

### b. Create a Virtual Environment
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### c. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### d. Configure Environment Variables
Copy the `.env.example` file to `.env` and update the values:
```bash
cp .env.example .env
```

Edit `.env` file with your database and email credentials.

---

## 2. Database Setup

### a. Create PostgreSQL Database
Create a database for the project:
```bash
psql -U postgres
CREATE DATABASE smartallot;
\q
```

### b. Run Migrations
Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### c. Create Superuser (Optional)
Create an admin user:
```bash
python manage.py createsuperuser
```

---

## 3. Running the Project

### a. Start Redis Server
Ensure Redis is running:
```bash
redis-server
```

### b. Start Development Server
Run the Django development server:
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

---

## 4. Running Tests

Run the test suite:
```bash
python manage.py test
```

---

## 5. Deployment

For deployment, use the provided build script:
```bash
bash build.sh
```

This will:
- Install dependencies
- Collect static files
- Run database migrations

---

## Project Features

- **Student Dashboard**: Students can view and manage their course allocations
- **Admin Dashboard**: Administrators can manage courses, rules, and view reports
- **Course Management**: Create, update, and delete courses
- **Rule Management**: Define allocation rules for minors and OE courses
- **Report Generation**: Download CSV reports of allocations

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This project is licensed under the MIT License.
