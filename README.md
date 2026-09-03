# Network & System Monitoring REST API

A lightweight, robust REST API built with Flask and SQLite for real-time system and network monitoring, historical metrics collection, and secure access management using JSON Web Tokens (JWT).

---

## Technologies

- **Python**: Primary programming language (Python 3.12+)
- **Flask**: Micro web framework for REST API routing and request handling
- **SQLite**: Serverless relational database for persistent metrics and user storage
- **PyJWT**: Secure authentication via JSON Web Tokens
- **bcrypt**: Password hashing and salt generation
- **psutil**: Cross-platform system and network telemetry gathering
- **pytest**: Automated unit and integration testing suite

---

## Features

- **JWT Authentication**: Stateless token-based security protecting sensitive endpoints.
- **User Registration & Login**: User credential management with salted bcrypt password hashing.
- **Protected Endpoints**: Endpoint access enforced with `@jwt_required` authorization decorators.
- **CPU Monitoring**: Real-time CPU core counts and usage percentage.
- **Memory Monitoring**: Total, used, available memory, and consumption percentages.
- **Disk Monitoring**: Cross-platform disk capacity, free space, and usage rates.
- **Network Interface Monitoring**: Details on network adapters, IP addresses, netmasks, and broadcast configurations.
- **Network Traffic Monitoring**: Live throughput counters (bytes sent/received, packets, errors, drops).
- **Historical Metrics & Persistence**: Periodic snapshot collection with limit-based historical query support stored in SQLite.
- **Automated Tests**: Pytest suite covering auth, monitoring, metrics, and error handling.
- **REST API Design**: Predictable JSON responses, standard HTTP status codes, and input validation.

---

## Project Structure

```text
network-monitoring-api/
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── database/
│   │   ├── db.py
│   │   └── schema.sql
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── metrics.py
│   │   ├── network.py
│   │   └── system.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── metrics_service.py
│   │   ├── network_service.py
│   │   └── system_service.py
│   └── utils/
│       └── security.py
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_metrics.py
    └── test_monitoring.py
```

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/ghazal-ansari/network-monitoring-api.git
cd network-monitoring-api
```

### 2. Create and activate a virtual environment

**On Windows (Git Bash):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration (Optional)
Copy `.env.example` to `.env` to configure your environment variables:
```bash
cp .env.example .env
```

### 5. Run the server
```bash
python run.py
```
The server will start at `http://127.0.0.1:5000`.

---

## API Documentation

All protected endpoints require the HTTP Authorization header:
```text
Authorization: Bearer <your_jwt_access_token>
```

---

### 1. Health Check
Checks the server and service health.

- **Method**: `GET`
- **Endpoint**: `/api/health`
- **Authentication**: None (Public)
- **Response**: `200 OK`
```json
{
  "status": "ok",
  "service": "network-monitoring-api"
}
```

---

### 2. User Registration
Registers a new user account with hashed password.

- **Method**: `POST`
- **Endpoint**: `/api/auth/register`
- **Authentication**: None (Public)
- **Request Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "username": "alice",
  "password": "strongpassword123"
}
```
- **Response**: `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "alice",
    "role": "user"
  }
}
```

---

### 3. User Login
Authenticates credentials and returns a JWT access token.

- **Method**: `POST`
- **Endpoint**: `/api/auth/login`
- **Authentication**: None (Public)
- **Request Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "username": "alice",
  "password": "strongpassword123"
}
```
- **Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "user": {
    "id": 1,
    "username": "alice",
    "role": "user"
  }
}
```

---

### 4. Get Current User Profile
Retrieves account information for the authenticated user.

- **Method**: `GET`
- **Endpoint**: `/api/auth/me`
- **Authentication**: Bearer Token (Protected)
- **Response**: `200 OK`
```json
{
  "id": 1,
  "username": "alice",
  "role": "user",
  "created_at": "2026-09-03 19:30:00"
}
```

---

### 5. Get System Metrics
Gathers live CPU, memory, disk, and operating system metrics.

- **Method**: `GET`
- **Endpoint**: `/api/system`
- **Authentication**: Bearer Token (Protected)
- **Response**: `200 OK`
```json
{
  "cpu": {
    "cores": 8,
    "usage_percent": 14.5
  },
  "memory": {
    "available": 8589934592,
    "total": 17179869184,
    "usage_percent": 50.0,
    "used": 8589934592
  },
  "disk": {
    "free": 107374182400,
    "total": 512110190592,
    "usage_percent": 79.0,
    "used": 404736008192
  },
  "system": {
    "hostname": "MY-PC",
    "operating_system": "Windows",
    "platform": "Windows-10-10.0.19045-SP0"
  }
}
```

---

### 6. Get Network Metrics
Gathers interface address details and live network traffic statistics.

- **Method**: `GET`
- **Endpoint**: `/api/network`
- **Authentication**: Bearer Token (Protected)
- **Response**: `200 OK`
```json
{
  "hostname": "MY-PC",
  "interfaces": [
    {
      "name": "Ethernet",
      "addresses": [
        {
          "address": "192.168.1.100",
          "broadcast": null,
          "family": "AddressFamily.AF_INET",
          "netmask": "255.255.255.0"
        }
      ]
    }
  ],
  "traffic": {
    "bytes_received": 104857600,
    "bytes_sent": 52428800,
    "dropped_in": 0,
    "dropped_out": 0,
    "errors_in": 0,
    "errors_out": 0,
    "packets_received": 95400,
    "packets_sent": 76200
  }
}
```

---

### 7. Collect and Store Metrics
Samples current CPU, memory, disk, and network stats, saving a snapshot to SQLite.

- **Method**: `POST`
- **Endpoint**: `/api/metrics/collect`
- **Authentication**: Bearer Token (Protected)
- **Response**: `201 Created`
```json
{
  "message": "Metrics collected successfully",
  "metrics": {
    "bytes_received": 104857600,
    "bytes_sent": 52428800,
    "cpu_usage": 15.2,
    "disk_usage": 79.0,
    "memory_usage": 50.1
  }
}
```

---

### 8. Get Latest Recorded Metric
Retrieves the most recent metrics snapshot stored in the database.

- **Method**: `GET`
- **Endpoint**: `/api/metrics/latest`
- **Authentication**: Bearer Token (Protected)
- **Response**: `200 OK`
```json
{
  "bytes_received": 104857600,
  "bytes_sent": 52428800,
  "cpu_usage": 15.2,
  "created_at": "2026-09-03 19:35:10",
  "disk_usage": 79.0,
  "id": 1,
  "memory_usage": 50.1
}
```

---

### 9. Get Historical Metrics
Retrieves a paginated list of historical metrics, sorted newest first.

- **Method**: `GET`
- **Endpoint**: `/api/metrics/history?limit=50`
- **Query Parameters**:
  - `limit` *(integer, optional, default: 50, min: 1, max: 100)*
- **Authentication**: Bearer Token (Protected)
- **Response**: `200 OK`
```json
{
  "count": 1,
  "metrics": [
    {
      "bytes_received": 104857600,
      "bytes_sent": 52428800,
      "cpu_usage": 15.2,
      "created_at": "2026-09-03 19:35:10",
      "disk_usage": 79.0,
      "id": 1,
      "memory_usage": 50.1
    }
  ]
}
```

---

## Testing

Execute the automated test suite with `pytest`:

```bash
pytest
```

Verbose output:
```bash
pytest -v
```

---

## Authentication Flow

1. Register a user:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "securepassword123"}'
   ```
2. Log in to receive a token:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "securepassword123"}'
   ```
3. Use the `access_token` in subsequent requests:
   ```bash
   curl -X GET http://127.0.0.1:5000/api/system \
     -H "Authorization: Bearer <access_token>"
   ```

---

## Security Considerations

- **Password Storage**: Passwords are never stored in plain text. They are hashed with salted bcrypt.
- **SQL Injection Prevention**: All queries use parameterized statements (`?`) with SQLite.
- **JWT Integrity**: Tokens are signed using HS256 with a 32+ byte key, and validated on every protected request.
- **Sensitive Data Exposure**: Password hashes are stripped before returning user objects.
- **Environment Isolation**: Production secrets and database paths are loaded from environment variables (`.env`).
