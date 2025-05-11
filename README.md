# Pixora API

A FastAPI application that provides authentication and user management functionality with MongoDB integration.

## Features

- User Authentication
  - Sign up with email and password
  - Login with JWT authentication
  - Password hashing for security
- User Management
  - User profile retrieval
  - Protected endpoints using JWT
- MongoDB Integration
  - Connects to MongoDB Atlas cluster
  - Stores user data securely

## Technologies Used

- FastAPI: Modern, fast web framework for building APIs
- MongoDB: NoSQL database for storing user data
- Motor: Asynchronous MongoDB driver for Python
- PyJWT: JSON Web Token implementation for Python
- Pydantic v2: Data validation and settings management
- Passlib & Bcrypt: Password hashing

## Project Structure

project/ │ ├── .env ├── main.py ├── requirements.txt │ ├── app/ │ ├── init.py │ ├── database.py │ │ │ ├── models/ │ │ ├── init.py │ │ └── user_model.py │ │ │ ├── auth/ │ │ ├── init.py │ │ ├── routes.py │ │ ├── jwt_handler.py │ │ └── password_handler.py │ │ │ └── user/ │ ├── init.py │ ├── routes.py │ └── utils.py


## API Endpoints

### Authentication

- **POST** `/api/auth/signup` - Register a new user
  - Body Parameters:
    - `first_name` (string): User's first name
    - `last_name` (string): User's last name
    - `email` (string): User's email
    - `password` (string): User's password (with validation rules)
    - `contact` (string): User's phone number
    - `birthday` (string): User's birthday (YYYY-MM-DD)
  - Returns: Success message with user ID

- **POST** `/api/auth/login` - Authenticate a user
  - Form Parameters:
    - `username` (string): User's email
    - `password` (string): User's password
  - Returns: JWT access token

### User Management

- **GET** `/api/users/me` - Get current user details
  - Headers: Bearer token
  - Returns: User profile data

- **GET** `/api/users/{user_id}` - Get user by ID
  - Headers: Bearer token
  - Returns: User profile data (only if requesting own profile)

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
3. 
