# Employee Management System API

A RESTful backend API for managing employee records, built with FastAPI, SQLAlchemy, and PostgreSQL. Includes JWT-based authentication and admin-level authorization.

---

## Tech Stack

- **Framework** — FastAPI
- **ORM** — SQLAlchemy
- **Database** — PostgreSQL
- **Authentication** — JWT (PyJWT)
- **Password Hashing** — pwdlib (Argon2)
- **Server** — Uvicorn

---

## Project Structure

```
application/
├── model/          # Pydantic models for request validation and response formatting
└── service/        # Core business logic

common/
├── config/         # Database and JWT configuration
├── error/          # Custom exceptions and exception handlers
└── middleware/     # Auth middleware and logger

controller/         # Route definitions (auth and employee endpoints)

repository/
├── entity/         # SQLAlchemy database models
└── /               # Database CRUD operations

main.py             # App entry point
```

---

## Authentication & Authorization

The API uses **JWT Bearer token** authentication.

- All `/employee` routes require a valid token
- Write operations (`create`, `update`, `delete`) require an **admin** token
- Read operations (`list`, `get by id`) are accessible to any authenticated user

### User Roles

| Role | Access |
|---|---|
| Regular user (`is_admin: false`) | GET endpoints only |
| Admin (`is_admin: true`) | All endpoints |

> Admin status is set directly in the database. New users always register as non-admin.

---

## API Endpoints

### Auth

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive JWT token | No |

### Employee

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/employee/` | List all employees (with filters) | Any user |
| GET | `/employee/{employee_id}` | Get employee by ID | Any user |
| POST | `/employee/create` | Create a new employee | Admin only |
| PUT | `/employee/update/{employee_id}` | Update an employee | Admin only |
| DELETE | `/employee/delete/{employee_id}` | Delete an employee | Admin only |

### System

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |

### Query Filters (GET `/employee/`)

| Parameter | Type | Description |
|---|---|---|
| `page` | int | Page number (default: 1) |
| `limit` | int | Results per page (default: 10, max: 100) |
| `first_name` | string | Filter by first name |
| `last_name` | string | Filter by last name |
| `designation` | string | Filter by designation |
| `email` | string | Filter by email |
| `phone` | string | Filter by phone |

---

## Environment Variables

Create a `.env` file at the root with the following:

```
DRIVERNAME=postgresql
USERNAME=your_db_username
PASSWORD=your_db_password
HOST=your_db_host
PORT=5432
DATABASE=your_db_name
SECRET_KEY=your_secret_key
TOKEN_EXPIRE_MINUTES=30
```

Generate a secure `SECRET_KEY` with:
```bash
openssl rand -hex 32
```

---

## Running Locally

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd employee_management_system
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your `.env` file** (see Environment Variables above)

**5. Run the server**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
Swagger UI at `http://localhost:8000/docs`

---

## Using the API (Swagger UI)

1. Register a user via `POST /auth/register`
2. Click the **Authorize** button (top right in `/docs`)
3. Enter your email and password and click **Authorize**
4. All subsequent requests will automatically include your token
5. To test admin routes, set `is_admin = true` for your user directly in the database

---

## Error Responses

All errors follow a consistent format:

```json
{
  "error": {
    "status_code": 404,
    "detail": "No employee found with ID 5."
  }
}
```

| Status Code | Meaning |
|---|---|
| 401 | Invalid or expired token / wrong credentials |
| 403 | Valid token but insufficient permissions |
| 404 | Employee not found |
| 409 | Duplicate record (email or phone) |
| 422 | Validation error (invalid request body) |
| 503 | Database unavailable |
| 500 | Unexpected server error |

---

## Deployment

The API is deployed on **Render** at:

```
https://your-service-name.onrender.com
```

> Note: The free tier spins down after 15 minutes of inactivity. The first request after inactivity may take 30–60 seconds to respond.
