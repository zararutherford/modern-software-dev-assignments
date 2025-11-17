# Immigration Client CRM - Django Version

A full-stack Django application for immigration attorneys to manage client cases. This version uses Python/Django for both backend and frontend (with Django templates), representing a non-JavaScript tech stack.

## Tech Stack

- **Backend**: Django 5.0 (Python)
- **Frontend**: Django Templates (HTML/CSS)
- **Database**: SQLite3 (Django ORM)
- **Form Handling**: Django Forms
- **Authentication**: Django built-in (for admin panel)

## Features

- **CRUD Operations**: Create, Read, Update, and Delete immigration client records
- **Client Management**: Track personal information, visa types, case status, and important dates
- **Validation**: Built-in form validation for email, phone numbers, and required fields
- **Admin Panel**: Django admin interface for advanced management
- **Case Tracking**: Monitor filing dates, priority dates, and case statuses
- **Visa Types**: Support for H-1B, L-1, O-1, EB-1/2/3, F-1, Green Card, Citizenship, Asylum, and more

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation & Setup

1. **Navigate to the project directory**:
   ```bash
   cd immigration-crm-django
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **(Optional) Create a superuser for admin access**:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

## Running the Application

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   - Main application: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/ (requires superuser account)

## Usage

### Main Application

1. **View All Clients**: The homepage displays all immigration clients in a table
2. **Add New Client**: Click "Add New Client" in the navigation bar
3. **View Client Details**: Click "View" on any client in the list
4. **Edit Client**: Click "Edit" on the client detail page
5. **Delete Client**: Click "Delete" on the client detail page (requires confirmation)

### Admin Panel

The Django admin panel at `/admin/` provides additional functionality:
- Bulk actions
- Advanced filtering and search
- Detailed field management
- Audit logs

## Project Structure

```
immigration-crm-django/
├── clients/                    # Main application
│   ├── migrations/            # Database migrations
│   ├── templates/clients/     # HTML templates
│   │   ├── base.html         # Base template with styling
│   │   ├── client_list.html  # List view
│   │   ├── client_detail.html # Detail view
│   │   ├── client_form.html  # Create/Update form
│   │   └── client_confirm_delete.html
│   ├── admin.py              # Admin configuration
│   ├── forms.py              # Django forms
│   ├── models.py             # Data models
│   ├── urls.py               # URL routing
│   └── views.py              # View functions
├── config/                    # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Data Model

The `Client` model includes:

**Personal Information**:
- First Name, Last Name
- Email, Phone
- Country of Origin

**Case Information**:
- Case Number (unique)
- Visa Type (H1B, L1, O1, EB1, EB2, EB3, F1, GREEN_CARD, CITIZENSHIP, ASYLUM, OTHER)
- Current Status (Initial Consultation, Documents Gathering, Application Prep, Filed, RFE, Approved, Denied, Withdrawn)
- Filing Date, Priority Date
- Notes

**Metadata**:
- Created At, Updated At (automatic)

## Environment Configuration

The application uses SQLite by default and includes sensible defaults for development. For production:

1. Create a `.env` file (see `.env.example`)
2. Set `SECRET_KEY` to a secure random value
3. Set `DEBUG=False`
4. Configure `ALLOWED_HOSTS`
5. Consider using PostgreSQL or MySQL instead of SQLite

## Testing

To test the application:

1. Create sample clients through the web interface or admin panel
2. Test CRUD operations:
   - Create a new client
   - View client list and details
   - Update client information
   - Delete a client

## Known Issues & Deviations

- This is a development setup using SQLite. For production, migrate to PostgreSQL/MySQL
- No user authentication on the main application (anyone can access)
- Form styling is inline CSS rather than separate stylesheet for simplicity
- Phone validation accepts international formats but doesn't format display

## Production Deployment

For production deployment:

1. Update `settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for secrets

2. Use a production database (PostgreSQL recommended)

3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

4. Use a production WSGI server (gunicorn, uWSGI)

5. Set up a reverse proxy (nginx, Apache)

## Additional Notes

- The application uses Django's built-in CSRF protection
- All forms include validation
- The ORM handles SQL injection prevention
- Admin panel provides audit trail via Django's logging system
