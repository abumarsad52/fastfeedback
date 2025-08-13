# FastFeedback - Feedback Management API

A modern, high-performance feedback management API built with FastAPI, SQLAlchemy, and PostgreSQL. This is a backend-only application that provides RESTful API endpoints for user authentication and feedback management.

> **Note:** This repository contains backend code only. No frontend or UI is included.

## ✨ Features

- 🚀 **FastAPI Backend**: High-performance, async API with automatic OpenAPI documentation
- 🔐 **User Authentication**: Secure login/register system with JWT tokens
- 💾 **PostgreSQL Database**: SQLAlchemy with async support and Alembic migrations
- 🛡️ **Security**: Password hashing with bcrypt, JWT token authentication
- 📝 **Feedback Management**: Full CRUD operations for user feedback
- 🔄 **Async Operations**: Built with async/await for optimal performance
- 📚 **API Documentation**: Automatic OpenAPI/Swagger documentation

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip
- Virtual environment (recommended)

### Quick Start

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd fastfeedback
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```

2. **Configure environment**
   Create a `.env` file:
   ```bash
   database_hostname=localhost
   database_port=5432
   database_username=your_username
   database_name=fastfeedback
   database_password=your_password
   secret_key=your-secret-key-here
   algorithm=HS256
   access_token_expires_minutes=30
   ```

3. **Setup database and run**
   ```bash
   # Create PostgreSQL database first
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

4. **Test the API**
   - API: `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy 2.0**: Async ORM with type hints
- **PostgreSQL**: Primary database with asyncpg driver
- **Alembic**: Database migration management
- **Pydantic**: Data validation and serialization
- **Python-Jose**: JWT token handling
- **Passlib**: Password hashing and verification

## 📁 Project Structure

```
fastfeedback/
├── alembic/                 # Database migrations
├── app/
│   ├── routes/             # API endpoints (auth, feedback)
│   ├── main.py             # FastAPI application
│   ├── models.py           # Database models
│   ├── schemas.py          # Data validation schemas
│   ├── database.py         # Database configuration
│   ├── config.py           # Environment settings
│   ├── oauth2.py           # JWT authentication
│   ├── utils.py            # Utility functions
│   └── exceptions.py       # Custom exceptions
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🔌 API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Feedback (`/feedback`)
- `POST /feedback/` - Create new feedback
- `GET /feedback/` - Get user's feedback list
- `GET /feedback/{id}` - Get specific feedback
- `PUT /feedback/{id}` - Update feedback
- `DELETE /feedback/{id}` - Delete feedback

## 📖 API Usage Examples

### User Registration
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=user@example.com&password=securepassword"
```

### Create Feedback (with authentication)
```bash
curl -X POST "http://localhost:8000/feedback/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "content=This is my feedback content"
```

## 🔧 Development

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🚀 Deployment

### Production Setup
1. Set production database credentials
2. Use production PostgreSQL instance
3. Enable HTTPS/SSL
4. Configure CORS restrictions
5. Implement rate limiting
6. Set up proper logging

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## 📚 Documentation

For detailed technical information:
- **API Docs**: Interactive documentation at `/docs`
- **Models & Schemas**: See `app/models.py` and `app/schemas.py`
- **Database**: Check `app/database.py` and `alembic/` folder

## 📄 License

This project is licensed under the MIT License.

## 💬 Support

- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the code examples above

---

**Built with ❤️ using FastAPI, SQLAlchemy, and PostgreSQL**
