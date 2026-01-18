# SmartAllot Project Structure

This document describes the organization of the SmartAllot project files.

## Directory Layout

```
Smartallot-Major-Minor-Allocation-System-/
│
├── smartallot/                    # Main Django project package
│   ├── __init__.py               # Python package marker
│   ├── settings.py               # Django settings and configuration
│   ├── urls.py                   # Root URL routing
│   ├── wsgi.py                   # WSGI application entry point
│   └── asgi.py                   # ASGI application entry point
│
├── allotment/                     # Django app for course allotment
│   ├── __init__.py               # Python package marker
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── forms.py                  # Django forms
│   ├── models.py                 # Database models
│   ├── tests.py                  # Unit tests
│   ├── urls.py                   # App-specific URL patterns
│   ├── utils.py                  # Utility functions
│   └── views.py                  # View functions/controllers
│
├── templates/                     # HTML templates
│   └── allotment/                # App-specific templates
│       ├── home.html             # Homepage template
│       ├── admin_dashboard.html  # Admin dashboard
│       ├── student_dashboard.html# Student dashboard
│       ├── manage_courses.html   # Course management page
│       ├── course_form.html      # Course creation/edit form
│       ├── rule_form.html        # Rule creation/edit form
│       ├── oe_rule_form.html     # OE rule form
│       └── confirm_delete.html   # Delete confirmation page
│
├── static/                        # Static files (CSS, JS, images)
│   └── (empty - ready for static assets)
│
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── build.sh                       # Build/deployment script
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git ignore patterns
├── README.md                     # Project documentation
└── test_env.py                   # Environment testing script
```

## File Organization Principles

### 1. **Main Project Package (`smartallot/`)**
Contains Django project-level configuration:
- **settings.py**: All Django settings, database config, installed apps
- **urls.py**: Root URL configuration that includes app URLs
- **wsgi.py/asgi.py**: Web server gateway interfaces

### 2. **App Package (`allotment/`)**
Contains the main application logic:
- **models.py**: Database models (Student, Course, Rules, etc.)
- **views.py**: Request handlers and business logic
- **forms.py**: Form definitions for user input
- **urls.py**: URL patterns specific to this app
- **admin.py**: Admin interface configuration
- **utils.py**: Helper functions and utilities

### 3. **Templates (`templates/`)**
HTML templates organized by app:
- Each app has its own subdirectory
- Templates are referenced as `allotment/template_name.html`

### 4. **Static Files (`static/`)**
Static assets like CSS, JavaScript, and images:
- Collected during deployment using `collectstatic`
- Organized by app or asset type

### 5. **Root Level Files**
- **manage.py**: Django's command-line utility
- **requirements.txt**: Project dependencies
- **build.sh**: Deployment build script
- **.env**: Environment-specific configuration
- **.gitignore**: Files to exclude from version control

## Running the Project

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Deployment
```bash
# Run build script
bash build.sh
```

## Adding New Features

### Adding a new view:
1. Define the view function in `allotment/views.py`
2. Create the template in `templates/allotment/`
3. Add URL pattern in `allotment/urls.py`

### Adding a new model:
1. Define the model in `allotment/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`

### Adding static files:
1. Place files in `static/` directory
2. Reference in templates: `{% static 'path/to/file' %}`
3. Collect static files: `python manage.py collectstatic`

## Benefits of This Structure

1. **Clear Separation of Concerns**: Project config vs. app logic
2. **Scalability**: Easy to add new apps or features
3. **Standard Django Layout**: Follows Django best practices
4. **Easy to Navigate**: Logical organization of related files
5. **Deployment Ready**: Proper structure for production deployment
