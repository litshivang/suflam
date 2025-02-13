# User Management API

## Overview

This project is a FastAPI-based CRUD API for managing user data with MySQL. It provides robust authentication and authorization using role-based access control:

- **Admin Users** can perform full CRUD operations.
- **Normal Users** can only view their own data.
- Secure password handling using bcrypt.
- Access tokens with a configurable TTL (Time-to-Live) are generated upon login.

## Features

- **CRUD Operations:** Create, Read, Update, Delete, and List users.  
- **Authentication:** User login with cellnumber and password.  
- **Authorization:** Role-based access (Admin vs. Normal User).  
- **Token Management:** Secure access token generation and storage.  
- **Error Handling:** Global exception handling for database integrity issues and other errors.  
- **Database:** MySQL with two tables: `user` and `accesstoken`.

## Tech Stack

- **Programming Language:** Python 3.9+  
- **Framework:** FastAPI  
- **Database ORM:** SQLAlchemy (with PyMySQL for MySQL)  
- **Authentication:** Passlib (bcrypt)  
- **Server:** Uvicorn  

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>


### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Database
Update the database credentials in `app/config.py` or create a `.env` file in the root directory with:
```env
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=fastapi_db
```

### 5. Create Database Tables
The tables are automatically created on application startup via:
```python
Base.metadata.create_all(bind=engine)
```
Alternatively, you can manually run the provided `create_tables.sql` script:
```bash
mysql -u your_username -p < create_tables.sql
```

### 6. Create an Admin User
To perform admin-only operations, create an admin user using the provided script:
```bash
python create_admin.py
```
This script creates an admin user with roleId `1`.

### 7. Run the Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

## API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Authentication
All endpoints (except login) require an `Authorization` header with a Bearer token:
```
Authorization: Bearer <access_token>
```

### Endpoints

#### 1. **User Login**
- **URL:** `/api/users/login`
- **Method:** `POST`
- **Description:** Authenticates a user using cellnumber and password. Returns an access token.
- **Request Body:**
  ```json
  {
    "cellnumber": "1234567890",
    "password": "your_password"
  }
  ```
- **Response Example:**
  ```json
  {
    "token": "P4ulxxF4zWn3Tl9ZMP1Pea5es1TF--dclawkuSsrS-E",
    "ttl": 30000,
    "userId": 4,
    "created": "2025-02-12T12:52:03"
  }
  ```

#### 2. **Create User (Admin Only)**
- **URL:** `/api/users`
- **Method:** `POST`
- **Description:** Creates a new user. This endpoint is restricted to admin users.
- **Headers:**
  ```
  Authorization: Bearer <admin_access_token>
  ```
- **Request Body:**
  ```json
  {
    "profilepic": "http://example.com/image.jpg",
    "name": "John Doe",
    "cellnumber": "0987654321",
    "password": "UserPassword123",
    "email": "johndoe@example.com",
    "roleId": 2
  }
  ```
- **Response:** Returns the created user object.

#### 3. **Get User by ID**
- **URL:** `/api/users/{id}`
- **Method:** `GET`
- **Description:** Retrieves details of a user. Admins can access any user's data, while normal users can only access their own data.
- **Headers:**
  ```
  Authorization: Bearer <access_token>
  ```
- **Response:** Returns the user object.

#### 4. **Update User (Admin Only)**
- **URL:** `/api/users/{id}`
- **Method:** `PATCH`
- **Description:** Updates user details.
- **Headers:**
  ```
  Authorization: Bearer <admin_access_token>
  ```
- **Request Body (Example):**
  ```json
  {
    "name": "John Updated"
  }
  ```
- **Response:** Returns the updated user object.

#### 5. **Delete User (Admin Only)**
- **URL:** `/api/users/{id}`
- **Method:** `DELETE`
- **Description:** Deletes a user by their ID.
- **Headers:**
  ```
  Authorization: Bearer <admin_access_token>
  ```
- **Response Example:**
  ```json
  {
    "detail": "User deleted successfully"
  }
  ```

#### 6. **List Users (Admin Only)**
- **URL:** `/api/users`
- **Method:** `GET`
- **Description:** Retrieves a list of all users.
- **Headers:**
  ```
  Authorization: Bearer <admin_access_token>
  ```
- **Response:** Returns an array of user objects.

## Error Handling
- **Integrity Errors:**  
  If duplicate entries (e.g., cellnumber or email) or other database integrity issues occur, the API returns an HTTP 400 with a detailed error message.
- **Unauthorized Access:**  
  When accessing restricted endpoints without the proper token, the API returns HTTP 401/403 errors.
- **General Errors:**  
  Unhandled exceptions are caught globally and return an HTTP 500 with error details.

## Testing
- **Using Postman:**  
  Test all endpoints by providing the required request bodies and headers.  
  - **Login:** Get an access token.
  - **Admin Operations:** Create, update, delete, and list users with an admin token.
  - **Normal User Access:** Verify that normal users can only access their own data.
- **Token Expiry:**  
  Validate token expiration by waiting beyond the TTL (e.g., 30 seconds) and verifying that expired tokens are rejected.

## Deployment
For production, consider containerizing the application with Docker or deploying on cloud platforms like AWS or Heroku. Ensure that environment variables are securely managed.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for any improvements or bug fixes.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please open an issue on GitHub.

```
