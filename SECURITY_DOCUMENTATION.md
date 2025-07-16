# Security Documentation

## Authentication Methods

### JWT Authentication (Main Application)

The main application uses JSON Web Tokens (JWT) for authentication:

1. **Token Generation**:
   - Tokens are generated when users register or log in
   - Tokens contain the user's ID as the identity claim
   - Tokens are signed with a secret key stored in environment variables

2. **Token Validation**:
   - All protected endpoints require a valid JWT token
   - Tokens are validated using the `@jwt_required()` decorator
   - User identity is retrieved using `get_jwt_identity()`

3. **Token Storage**:
   - Tokens are stored in the client's localStorage
   - Tokens are included in the Authorization header for API requests

4. **Token Configuration**:
   ```python
   app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
   app.config['JWT_TOKEN_LOCATION'] = ['headers']
   app.config['JWT_HEADER_NAME'] = 'Authorization'
   app.config['JWT_HEADER_TYPE'] = 'Bearer'
   ```

### OAuth Authentication (Google)

The application supports Google OAuth for user authentication:

1. **OAuth Configuration**:
   - Client ID and Secret are stored in environment variables
   - Redirect URI is configured to `/auth/google/callback`

2. **OAuth Flow**:
   - User is redirected to Google for authentication
   - Google redirects back with an authorization code
   - Application exchanges code for access token
   - User information is retrieved from Google API

3. **User Creation/Linking**:
   - If user with Google ID exists, log them in
   - If user with same email exists, link Google ID
   - Otherwise, create a new user account

### Bearer Token Authentication (CRM Application)

The CRM application uses a static Bearer token for API authentication:

1. **Token Configuration**:
   - Token is stored in environment variables
   - Token is validated for all protected endpoints

2. **Token Validation**:
   ```python
   def validate_bearer_token(token):
       expected_token = os.getenv('CRM_BEARER_TOKEN', 'secure-bearer-token-123')
       return token == f'Bearer {expected_token}'
   ```

3. **Token Usage**:
   - Token is included in the Authorization header for API requests
   - Token is required for all CRM API endpoints

## Password Security

1. **Password Hashing**:
   - Passwords are hashed using bcrypt
   - Salt is automatically generated and included in the hash

2. **Password Validation**:
   - Passwords are validated by comparing hashes
   - Original passwords are never stored

## Cross-Origin Resource Sharing (CORS)

1. **CORS Configuration**:
   - CORS is enabled for both applications
   - Allowed origins are configured to allow cross-domain requests

2. **CORS Headers**:
   - Access-Control-Allow-Origin
   - Access-Control-Allow-Methods
   - Access-Control-Allow-Headers

## Input Validation

1. **Request Validation**:
   - All API endpoints validate required fields
   - Data types and formats are validated
   - Invalid requests return appropriate error responses

2. **SQL Injection Prevention**:
   - SQLAlchemy ORM is used for database operations
   - Parameterized queries prevent SQL injection

## Error Handling

1. **Authentication Errors**:
   - 401 Unauthorized for invalid/missing tokens
   - Custom error messages for different authentication failures

2. **Validation Errors**:
   - 400 Bad Request for invalid input
   - Detailed error messages for validation failures

3. **Server Errors**:
   - 500 Internal Server Error for unexpected errors
   - Error logging for debugging

## Environment Variables

Sensitive configuration is stored in environment variables:

1. **Main Application**:
   - SECRET_KEY
   - JWT_SECRET_KEY
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET
   - DATABASE_URL

2. **CRM Application**:
   - SECRET_KEY
   - CRM_BEARER_TOKEN

## Security Recommendations

1. **Production Deployment**:
   - Use HTTPS for all communication
   - Set secure and httpOnly flags for cookies
   - Implement rate limiting for authentication endpoints
   - Use a production-grade WSGI server

2. **Token Security**:
   - Implement token refresh mechanism
   - Add token expiration and revocation
   - Store tokens securely (httpOnly cookies preferred over localStorage)

3. **Additional Security Measures**:
   - Implement two-factor authentication
   - Add IP-based rate limiting
   - Implement account lockout after failed login attempts