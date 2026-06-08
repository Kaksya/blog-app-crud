# Blog App CRUD

A Django REST Framework-based blog application with CRUD operations support.

## Project Overview

This project provides a REST API for managing blog posts with full Create, Read, Update, and Delete (CRUD) functionality. It's built with Django and Django REST Framework, with JWT authentication support for secure API access.

## Tech Stack

- **Framework**: Django 6.0.6
- **API**: Django REST Framework 3.17.1
- **Authentication**: djangorestframework-simplejwt 5.5.1
- **Database**: SQLite (configurable)
- **Python**: 3.x
- **Type Checking**: MyPy with Django stubs

## Project Structure

```
blog-app-crud/
├── app/                    # Main application
│   ├── migrations/        # Database migrations
│   ├── models.py          # Data models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Django admin configuration
│   └── ai_utils.py        # AI utility functions
├── blog/                   # Django project settings
│   ├── settings.py        # Project settings
│   ├── urls.py            # Project URL routing
│   ├── asgi.py            # ASGI configuration
│   └── wsgi.py            # WSGI configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── mypy.ini              # MyPy configuration
└── db.sqlite3            # SQLite database (generated)
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blog-app-crud
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows
   # or
   source env/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Endpoints

The following endpoints are available for blog management:

- `GET /api/` - List all endpoints
- `GET /api/posts/` - List all blog posts
- `POST /api/posts/` - Create a new blog post
- `GET /api/posts/{id}/` - Retrieve a specific blog post
- `PUT /api/posts/{id}/` - Update a blog post
- `PATCH /api/posts/{id}/` - Partially update a blog post
- `DELETE /api/posts/{id}/` - Delete a blog post

## Authentication

This project uses JWT (JSON Web Tokens) for API authentication. To use protected endpoints:

1. Obtain a token via the login endpoint
2. Include the token in the Authorization header:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root to configure environment-specific settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings File

Main configuration is in `blog/settings.py`. Key settings include:
- `DEBUG` - Debug mode (set to False in production)
- `ALLOWED_HOSTS` - Allowed host names
- `INSTALLED_APPS` - Registered Django apps
- `DATABASES` - Database configuration

## Development

### Type Checking

Run MyPy for static type checking:

```bash
mypy .
```

### Running Tests

```bash
python manage.py test
```

### Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` with your superuser credentials.

## Database

The project uses SQLite by default. To reset the database:

```bash
# Delete the db.sqlite3 file and migrations
rm db.sqlite3

# Rerun migrations
python manage.py migrate
```

## Contributing

1. Create a new branch for your feature
2. Make your changes with descriptive commits
3. Ensure code passes type checking with mypy
4. Submit a pull request

## Security Notes

- Never commit `.env` files with sensitive data
- Always set `DEBUG=False` in production
- Rotate your `SECRET_KEY` in production
- Use environment variables for sensitive configuration

## Troubleshooting

### Import Errors
If you encounter import errors, ensure your virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Errors
If you have database migration issues:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Port Already in Use
If port 8000 is already in use:
```bash
python manage.py runserver 8001
```

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please create an issue in the repository or contact the project maintainers.
