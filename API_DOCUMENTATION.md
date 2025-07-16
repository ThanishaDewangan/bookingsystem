# API Documentation

## Main Application API

### Authentication

#### Register User
- **URL**: `/api/register`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "access_token": "jwt_token_here",
      "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
    ```

#### Login User
- **URL**: `/api/login`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "access_token": "jwt_token_here",
      "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
    ```

#### Google OAuth Login
- **URL**: `/auth/google`
- **Method**: `GET`
- **Auth Required**: No
- **Success**: Redirects to Google OAuth flow

### Events

#### Get All Events
- **URL**: `/api/events`
- **Method**: `GET`
- **Auth Required**: Yes (JWT)
- **Headers**:
  ```
  Authorization: Bearer <jwt_token>
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "title": "Morning Meditation Session",
        "description": "Start your day with mindfulness",
        "event_type": "session",
        "date_time": "2023-07-15T09:00:00Z",
        "duration": 60,
        "max_participants": 15,
        "price": 25.0,
        "facilitator": "Dr. Sarah Johnson",
        "available_spots": 12
      }
    ]
    ```

#### Get Event by ID
- **URL**: `/api/events/<event_id>`
- **Method**: `GET`
- **Auth Required**: Yes (JWT)
- **Headers**:
  ```
  Authorization: Bearer <jwt_token>
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "title": "Morning Meditation Session",
      "description": "Start your day with mindfulness",
      "event_type": "session",
      "date_time": "2023-07-15T09:00:00Z",
      "duration": 60,
      "max_participants": 15,
      "price": 25.0,
      "facilitator": "Dr. Sarah Johnson",
      "available_spots": 12
    }
    ```

### Bookings

#### Create Booking
- **URL**: `/api/bookings`
- **Method**: `POST`
- **Auth Required**: Yes (JWT)
- **Headers**:
  ```
  Authorization: Bearer <jwt_token>
  ```
- **Body**:
  ```json
  {
    "event_id": 1
  }
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "booking_id": 1,
      "message": "Booking confirmed successfully"
    }
    ```

#### Get User Bookings
- **URL**: `/api/my-bookings`
- **Method**: `GET`
- **Auth Required**: Yes (JWT)
- **Headers**:
  ```
  Authorization: Bearer <jwt_token>
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "event": {
          "id": 1,
          "title": "Morning Meditation Session",
          "date_time": "2023-07-15T09:00:00Z",
          "event_type": "session"
        },
        "booking_date": "2023-07-10T14:30:00Z",
        "status": "confirmed",
        "is_upcoming": true
      }
    ]
    ```

#### Cancel Booking
- **URL**: `/api/bookings/<booking_id>`
- **Method**: `DELETE`
- **Auth Required**: Yes (JWT)
- **Headers**:
  ```
  Authorization: Bearer <jwt_token>
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "message": "Booking cancelled successfully"
    }
    ```

## CRM Application API

### Notifications

#### Receive Booking Notification
- **URL**: `/notify`
- **Method**: `POST`
- **Auth Required**: Yes (Bearer Token)
- **Headers**:
  ```
  Authorization: Bearer <crm_bearer_token>
  Content-Type: application/json
  ```
- **Body**:
  ```json
  {
    "booking_id": 1,
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    "event": {
      "id": 1,
      "title": "Morning Meditation Session",
      "date_time": "2023-07-15T09:00:00Z"
    },
    "facilitator_id": 1
  }
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "status": "success",
      "message": "Booking notification received and processed",
      "notification_id": 1
    }
    ```

#### Get All Notifications
- **URL**: `/notifications`
- **Method**: `GET`
- **Auth Required**: Yes (Bearer Token)
- **Headers**:
  ```
  Authorization: Bearer <crm_bearer_token>
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "booking_id": 1,
        "user_name": "John Doe",
        "user_email": "john@example.com",
        "event_title": "Morning Meditation Session",
        "event_date": "2023-07-15T09:00:00Z",
        "facilitator_id": 1,
        "received_at": "2023-07-10T14:30:00Z",
        "processed": false
      }
    ]
    ```

#### Mark Notification as Processed
- **URL**: `/notifications/<notification_id>/process`
- **Method**: `POST`
- **Auth Required**: Yes (Bearer Token)
- **Headers**:
  ```
  Authorization: Bearer <crm_bearer_token>
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "status": "success",
      "message": "Notification marked as processed"
    }
    ```

### Facilitator Events

#### Get Facilitator Events
- **URL**: `/api/facilitator/events/<facilitator_id>`
- **Method**: `GET`
- **Auth Required**: Yes (Bearer Token)
- **Headers**:
  ```
  Authorization: Bearer <crm_bearer_token>
  ```
- **Success Response**: 
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "title": "Morning Meditation Session",
        "date_time": "2023-07-15T09:00:00Z",
        "bookings_count": 3,
        "max_participants": 15,
        "is_active": true
      }
    ]
    ```

## Security Implementation

### JWT Authentication
- Used for securing the main application API
- Token issued on login/registration
- Required for all protected endpoints
- Expiration time: 24 hours

### Bearer Token Authentication
- Used for securing communication between main app and CRM
- Static token stored in environment variables
- Required for all CRM API endpoints

## Error Responses

### Authentication Error
- **Code**: 401
- **Content**: 
  ```json
  {
    "error": "Unauthorized",
    "message": "Invalid or missing token"
  }
  ```

### Validation Error
- **Code**: 400
- **Content**: 
  ```json
  {
    "error": "Bad Request",
    "message": "Missing required field: field_name"
  }
  ```

### Resource Not Found
- **Code**: 404
- **Content**: 
  ```json
  {
    "error": "Not Found",
    "message": "The requested resource was not found"
  }
  ```

### Server Error
- **Code**: 500
- **Content**: 
  ```json
  {
    "error": "Internal Server Error",
    "message": "An unexpected error occurred"
  }
  ```