# Project Setup and Usage Guide

## Overview
K2 FastAPI challenge

---

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- SQLite (comes pre-installed with Python)

---

## Installation

### 1. Clone this Repository
```shell
git clone https://github.com/ramonbss/k2_fastapi.git
cd k2_fastapp
```

### 2. Set the Virtual Environment
```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 3. Setting credencials
Create an .env file at the root of the project or set environment variables at system or container level following the naming in the file "dot_env_Template"

---

## Database
- For simplicity, sqlite is being used.  
- FastApi automatically manage the database for us. The tables will be created automatically when you run the application.  
- The project uses an **in-memory SQLite database** for testing. 

---

## Running the Application

To start the application, use the following command:
```shell
python run_api.py
```

This will start the server on [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Endpoints

### User Purchases

#### Endpoint
**GET /user**

#### Description
Fetches the purchases of an user given the `user_id`.

#### Parameters
- **Query Parameter**: `user_id` (integer, required)  
  The unique identifier of the user.

#### Curl Example
```shell
curl -X GET "http://127.0.0.1:8000/user?user_id=1"
-H "Content-Type: application/json"
```

#### Example Response
```json
{
    "purchases": [
        {
            "id": 1,
            "item": "Laptop",
            "price": 2500.0
        },
        {
            "id": 2,
            "item": "Smartphone",
            "price": 1200.0
        }
    ]
}
```

### Admin Reports

#### Endpoint
**GET /admin**

#### Description
Fetches the reports of an admin based on their `user_id`.

#### Parameters
- **Query Parameter**: `user_id` (integer, required)  
  The unique identifier of the admin.


#### Curl Example
```shell
curl -X GET "http://127.0.0.1:8000/admin?user_id=1"
-H "Content-Type: application/json"
```

#### Example Response
```json
{
    "reports": [
        {
            "id": 1,
            "title": "Monthly Sales",
            "status": "Completed"
        },
        {
            "id": 2,
            "title": "User Activity",
            "status": "Pending"
        }
    ]
}
```

