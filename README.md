# Property Listing Backend

This project is a Django-based backend for managing property listings, designed to be consumed by a Next.js frontend application.

## Project Structure

- **listings/**: Contains the main application for managing property listings.

  - **models.py**: Defines the data models for properties.
  - **views.py**: Contains the views for handling requests related to property listings.
  - **serializers.py**: Provides serializers for converting model instances to JSON.
  - **admin.py**: Registers models with the Django admin site.
  - **tests.py**: Contains tests for the application.
  - **migrations/**: Directory for database migrations.

- **base/**: The main Django project directory.

  - **settings.py**: Configuration settings for the Django project.
  - **urls.py**: URL routing for the application.
  - **asgi.py**: ASGI configuration for asynchronous support.
  - **wsgi.py**: WSGI configuration for deployment.

- **manage.py**: Command-line utility for managing the Django project.

## Setup Instructions

1. **Clone the repository**:

   ```
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment**:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Run migrations**:

   ```
   python manage.py migrate
   ```

5. **Start the development server**:
   ```
   python manage.py runserver
   ```

## Usage

- Access the API at `http://localhost:8000/api/` to interact with property listings.
- Use the Django admin interface at `http://localhost:8000/admin/` to manage properties.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.
