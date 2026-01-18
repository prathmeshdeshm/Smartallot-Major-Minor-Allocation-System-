# Quick Start Guide

This is a quick reference for getting the SmartAllot project up and running after the reorganization.

## File Structure Overview

```
smartallot/           ← Project configuration (settings, URLs)
allotment/            ← Application code (models, views, forms)
templates/allotment/  ← HTML templates
static/               ← CSS, JavaScript, images
manage.py             ← Django management commands
```

## Quick Setup (3 Steps)

### 1. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings (database, email, etc.)
nano .env  # or use your preferred editor
```

### 2. Install & Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser
```

### 3. Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Common Commands

```bash
# Run development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

## Project Structure Details

### Main Configuration (`smartallot/`)
- `settings.py` - All Django settings
- `urls.py` - Root URL configuration
- `wsgi.py` / `asgi.py` - Server interfaces

### Application (`allotment/`)
- `models.py` - Database models (Student, etc.)
- `views.py` - View functions (handlers)
- `forms.py` - Form definitions
- `urls.py` - URL patterns
- `admin.py` - Admin interface config

### Templates (`templates/allotment/`)
- `home.html` - Homepage
- `admin_dashboard.html` - Admin panel
- `student_dashboard.html` - Student panel
- `manage_courses.html` - Course management
- Other forms and pages

## Troubleshooting

**Problem**: ModuleNotFoundError: No module named 'django'
**Solution**: Run `pip install -r requirements.txt`

**Problem**: Database connection error
**Solution**: Check `.env` database settings (DB_NAME, DB_USER, DB_PASSWORD, etc.)

**Problem**: Templates not found
**Solution**: Templates are now in `templates/allotment/` - Django is configured to look there

**Problem**: Static files not loading
**Solution**: Run `python manage.py collectstatic` for production

## Development Workflow

1. Make changes to code
2. Run `python manage.py check` to verify
3. If models changed: `python manage.py makemigrations` and `python manage.py migrate`
4. Test with `python manage.py runserver`
5. Commit changes to git

## Need More Help?

See detailed documentation in:
- `README.md` - Complete setup guide
- `PROJECT_STRUCTURE.md` - Detailed structure explanation
- `REORGANIZATION_SUMMARY.md` - What changed in the reorganization
