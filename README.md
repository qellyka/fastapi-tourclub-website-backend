# Hiking Club Management API

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.43-green.svg)](https://www.sqlalchemy.org/)

A comprehensive REST API for managing hiking club activities, including hike reports, pass registrations, participant management, and file storage integration.

## 🚀 Features

- **User Management**: Registration, authentication, profile management with role-based access control
- **Hike Management**: Create, read, update, delete hike reports with GPX route support
- **Pass Registry**: Mountain pass database with difficulty ratings and geographical data
- **Participant Tracking**: Manage club members and hike participants with roles
- **File Storage**: S3-compatible storage for reports, routes, and media files
- **Email Integration**: Automated email verification and notifications
- **GeoJSON Support**: Convert GPX files to GeoJSON for mapping integration

## 🏗️ Architecture

### Tech Stack

- **Backend Framework**: FastAPI 0.116+
- **Database**: PostgreSQL 15+ with AsyncPG driver
- **ORM**: SQLAlchemy 2.0+ (async)
- **Authentication**: JWT with refresh tokens
- **File Storage**: S3-compatible object storage
- **Email**: SMTP with HTML templates
- **Containerization**: Docker with Docker Compose

### Project Structure

```
├── api/                    # API endpoints
│   └── v1/                # API version 1
├── core/                  # Core configuration and utilities
├── crud/                  # Database operations
├── db/                    # Database configuration
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic schemas
├── services/              # External service integrations
└── templates/             # Email templates
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- PostgreSQL 15+ (if running without Docker)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-tourclub-website-backend
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

The API will be available at `http://localhost:8000`

### Local Development

1. **Install dependencies**
   ```bash
   poetry install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

3. **Run database migrations**
   ```bash
   # Database tables are auto-created on startup
   python main.py
   ```

4. **Start development server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DEBUG` | Enable debug mode | No | `false` |
| `HOST` | Server host | No | `0.0.0.0` |
| `PORT` | Server port | No | `8000` |
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `SECRET_KEY` | JWT secret key | Yes | - |
| `MAIL_USERNAME` | SMTP username | Yes | - |
| `MAIL_PASSWORD` | SMTP password | Yes | - |
| `S3_ACCESS_KEY` | S3 access key | Yes | - |
| `S3_SECRET_KEY` | S3 secret key | Yes | - |

### Database Configuration

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/hiking_club
```

### S3 Storage Configuration

```env
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_ENDPOINT_URL=https://s3.amazonaws.com
S3_HIKE_MEDIA_BUCKET_NAME=expedition-reports
S3_USER_MEDIA_BUCKET_NAME=member-profiles
```

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/refresh` - Refresh access token
- `GET /api/auth/verify` - Email verification

### Archive Endpoints

- `GET /api/archive/hikes` - List all hikes
- `POST /api/archive/hikes` - Create new hike report
- `GET /api/archive/hikes/{id}` - Get hike by ID
- `DELETE /api/archive/hikes/{id}` - Delete hike
- `GET /api/archive/hikes/{id}/file/{type}` - Download hike files

### Pass Registry Endpoints

- `GET /api/archive/passes` - List all passes
- `POST /api/archive/passes` - Create new pass
- `GET /api/archive/passes/{id}` - Get pass by ID
- `GET /api/archive/passes/{id}/hikes` - Get hikes for pass

### User Management Endpoints

- `GET /api/users` - List users (admin only)
- `GET /api/users/{id}` - Get user by ID
- `DELETE /api/users/{id}` - Delete user
- `GET /api/users/me` - Get current user profile

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Authentication & Authorization

### JWT Token System

The API uses JWT tokens with the following flow:

1. **Registration/Login**: Returns access and refresh tokens
2. **Access Token**: Short-lived (30 minutes), used for API requests
3. **Refresh Token**: Long-lived (7 days), used to generate new access tokens
4. **Cookies**: Tokens are stored in HTTP-only cookies for security

### Role-Based Access Control

- **guest**: Basic read access to public content
- **admin**: Full access to all endpoints and user management

### Security Features

- Password hashing with bcrypt
- HTTP-only cookies for token storage
- Email verification for new accounts
- Token rotation on refresh
- Secure cookie settings in production

## 🗄️ Database Schema

### Core Models

- **UserModel**: User accounts and authentication
- **HikeModel**: Hiking expedition reports
- **PassModel**: Mountain pass registry
- **HikeParticipantModel**: Hike participation tracking
- **ClubParticipantModel**: Club membership management
- **TokenModel**: Refresh token storage

### Relationships

- Users can participate in multiple hikes
- Hikes can traverse multiple passes
- Many-to-many relationships with association tables
- Cascade deletes for data integrity

## 📁 File Management

### Supported File Types

- **GPX Files**: Route data (converted to GeoJSON)
- **PDF Files**: Expedition reports
- **Images**: User avatars and photos (JPEG, PNG, GIF, WebP)

### Storage Integration

- S3-compatible object storage
- Separate buckets for different content types
- Secure file uploads with content type validation
- Direct file streaming for downloads

## 🧪 Development

### Code Quality

The project follows Python best practices:

- **Type Hints**: Full type annotation coverage
- **Async/Await**: Asynchronous database and file operations
- **Pydantic Models**: Request/response validation
- **SQLAlchemy 2.0**: Modern ORM with async support


### Code Formatting

```bash
# Format code
black .

# Check formatting
black --check .
```

## 🚀 Deployment

### Docker Production Build

```dockerfile
FROM python:3.12.10-slim

# Install Poetry and dependencies
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy application
COPY . .

# Run application
CMD ["python", "main.py"]
```

### Environment Considerations

- Set `DEBUG=false` in production
- Use secure `SECRET_KEY` (256-bit)
- Enable `COOKIE_SECURE=true` for HTTPS
- Configure proper CORS origins
- Set up SSL/TLS termination
- Use connection pooling for database

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Check the [API documentation](http://localhost:8000/docs)
- Review the [database schema](#schemas)

## 📝 Changelog

### Version 0.1.0
- Initial release
- User authentication and management
- Hike and pass registry
- File upload and storage
- Email verification system

**Project Maintainer**: Pronyakin Egor Andreevich  
**Support**: [Issue Tracker](https://github.com/qellyka/fastapi-tourclub-website-backend/issues)