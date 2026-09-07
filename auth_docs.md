Authentication

## Overview

The API uses JWT (JSON Web Tokens) for authentication. Passwords are hashed with bcrypt before being stored in the database.

## Authentication Components

app/models/auth_user.py

- Defines the users database table:

    id — primary key
    users_name — unique username
    email — unique email
    hashed_password — bcrypt password hash

Passwords are never stored as plain text.
app/schemas/auth.py

- Defines the request and response models:

    RegisterRequest — name, email, password
    LoginRequest — email and password
    TokenResponse — JWT access token and token type

## Password Security

- app/utils/security.py provides:

- hash_password(password)

- Hashes a password using bcrypt.

- verify_password(plain, hashed)

- Checks a supplied password against the stored hash.

Example:

python -c "from app.utils.security import hash_password; print(hash_password('TestPass123'))"

JWT Tokens

JWT creation is handled by:

create_access_token(data)

The token contains the user's ID as the sub claim and expires after 30 minutes.





The application uses:

Algorithm: HS256
Expiration: 30 minutes


## Endpoint:

POST /auth/register

The registration process:

    Checks whether the email already exists.
    Hashes the password with bcrypt.
    Creates the user.
    Saves the user to SQLite.
    Generates a JWT.
    Returns the token.

Example request:

{
  "name": "Tom Sellick",
  "email": "sellick@example.com",
  "password": "TestPass123"
}

Response:

{
  "access_token": "eyJ...",
  "token_type": "bearer"
}

Login

Endpoint:

POST /auth/login

The login process:

    Finds the user by email.
    Verifies the password against the stored bcrypt hash.
    Creates a new JWT.
    Returns the token.

Example:

{
  "email": "sellick@example.com",
  "password": "TestPass123"
}

Current User

get_current_user() in app/utils/security.py validates the JWT.

It:

    Reads the Bearer token from the Authorization header.
    Decodes and validates the JWT.
    Gets the user ID from the sub claim.
    Looks up the user in the database.
    Returns the authenticated user.
    Raises 401 Unauthorized if the token is invalid, expired, or the user doesn't exist.

The header must use:

Authorization: Bearer <token>

Not simply:

Authorization: <token>

Protected Student Endpoints

Authentication was added only where required:

GET    /students              Public

GET    /students/{id}         Protected
POST   /students              Protected
PATCH  /students/{id}         Protected
DELETE /students/{id}         Protected

## Protected endpoints use:

Depends(get_current_user)

The returned user is currently used only to verify authentication; the endpoint does not yet use the user's identity for authorization.
Testing

Generate a token:



Then use the token with a protected request:

curl -X POST "http://127.0.0.1:8000/students" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN"

Without a valid token, protected endpoints return:

401 Unauthorized

A successful authenticated request returns the normal endpoint response.