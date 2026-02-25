# BHUKK Manufacturers Backend API

FastAPI backend for managing manufacturers information with PostgreSQL database.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Setup Instructions for macOS

### 1. Clone the Repository

```bash
git clone <repository-url>
cd bhukk_website_backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Edit the `.env` file with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/bhukk_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bhukk_db
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### 6. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE bhukk_db;

# Exit psql
\q
```

### 7. Start the Backend Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Manufacturers

- `POST /api/manufacturers/create` - Create new manufacturer
- `GET /api/manufacturers/all` - Get all manufacturers
- `GET /api/manufacturers/{manufacturer_id}` - Get manufacturer by ID
- `PUT /api/manufacturers/{manufacturer_id}` - Update manufacturer
- `DELETE /api/manufacturers/{manufacturer_id}` - Delete manufacturer

## Project Structure

```
bhukk_website_backend/
├── main.py                           # Main FastAPI application
├── db.py                             # Database configuration
├── requirements.txt                  # Python dependencies
├── .env                              # Environment variables
├── README.md                         # This file
├── models/
│   └── manufacturers/
│       └── manufacturers_models.py   # Database models
├── routes/
│   └── manufacturers/
│       └── manufacturers_routes.py   # API routes
├── services/
│   └── manufacturers/
│       └── manufacturers_file_uploads.py  # File handling service
└── uploads/                          # Uploaded files directory
    └── manufacturers/
        └── {manufacturer_id}/
```

## File Upload

- Supported formats: PDF, JPG, JPEG, PNG
- Images are automatically compressed for optimization
- Files are stored in `/uploads/manufacturers/{manufacturer_id}/`

## Deactivate Virtual Environment

```bash
deactivate
```

## Troubleshooting

### Database connection error
- Ensure PostgreSQL is running
- Verify credentials in `.env` file
- Check if database exists

### Port already in use
- Change `SERVER_PORT` in `.env` file
- Or kill process using port 8000:
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```

## Development

### Run in development mode

```bash
source venv/bin/activate
python main.py
```

### Run with auto-reload

```bash
uvicorn main:app --reload
```

## Support

For issues or questions, please contact the development team.
