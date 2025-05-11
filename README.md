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
