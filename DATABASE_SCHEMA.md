# Database Schema

## Main Application Database

### User
Stores information about registered users.

| Column      | Type         | Constraints       | Description                    |
|-------------|--------------|-------------------|--------------------------------|
| id          | Integer      | Primary Key       | Unique identifier for the user |
| name        | String(100)  | Not Null         | User's full name               |
| email       | String(120)  | Unique, Not Null | User's email address           |
| password    | String(200)  | Not Null         | Hashed password                |
| google_id   | String(100)  | Nullable         | Google OAuth ID if applicable  |
| created_at  | DateTime     | Default: now      | Account creation timestamp     |

### Facilitator
Stores information about session/retreat facilitators.

| Column      | Type         | Constraints       | Description                          |
|-------------|--------------|-------------------|--------------------------------------|
| id          | Integer      | Primary Key       | Unique identifier for the facilitator|
| name        | String(100)  | Not Null         | Facilitator's full name              |
| email       | String(120)  | Unique, Not Null | Facilitator's email address          |
| bio         | Text         | Nullable         | Facilitator's biography              |
| specialties | String(200)  | Nullable         | Facilitator's areas of expertise     |

### Event
Stores information about available sessions and retreats.

| Column           | Type         | Constraints                | Description                           |
|------------------|--------------|----------------------------|---------------------------------------|
| id               | Integer      | Primary Key                | Unique identifier for the event       |
| title            | String(200)  | Not Null                  | Event title                           |
| description      | Text         | Not Null                  | Event description                     |
| event_type       | String(50)   | Not Null                  | Type: 'session' or 'retreat'          |
| date_time        | DateTime     | Not Null                  | Event date and time                   |
| duration         | Integer      | Not Null                  | Duration in minutes                   |
| max_participants | Integer      | Not Null                  | Maximum number of participants        |
| price            | Float        | Not Null                  | Event price                           |
| facilitator_id   | Integer      | Foreign Key (Facilitator) | Reference to the event facilitator    |
| is_active        | Boolean      | Default: True             | Whether the event is active/available |

### Booking
Stores information about user bookings.

| Column      | Type         | Constraints           | Description                        |
|-------------|--------------|------------------------|-----------------------------------|
| id          | Integer      | Primary Key           | Unique identifier for the booking |
| user_id     | Integer      | Foreign Key (User)    | Reference to the booking user     |
| event_id    | Integer      | Foreign Key (Event)   | Reference to the booked event     |
| booking_date| DateTime     | Default: now          | When the booking was made         |
| status      | String(20)   | Default: 'confirmed'  | Booking status                    |

## CRM Application Database

### BookingNotification
Stores notifications about bookings for facilitators.

| Column         | Type         | Constraints          | Description                           |
|----------------|--------------|----------------------|---------------------------------------|
| id             | Integer      | Primary Key          | Unique identifier for the notification|
| booking_id     | Integer      | Not Null            | Reference to the booking              |
| user_name      | String(100)  | Not Null            | Name of the user who booked           |
| user_email     | String(120)  | Not Null            | Email of the user who booked          |
| event_title    | String(200)  | Not Null            | Title of the booked event             |
| event_date     | DateTime     | Not Null            | Date and time of the event            |
| facilitator_id | Integer      | Not Null            | Reference to the facilitator          |
| received_at    | DateTime     | Default: now         | When the notification was received    |
| processed      | Boolean      | Default: False       | Whether the notification is processed |

## Relationships

1. **User to Booking**: One-to-Many
   - A user can have multiple bookings
   - Each booking belongs to one user

2. **Event to Booking**: One-to-Many
   - An event can have multiple bookings
   - Each booking is for one event

3. **Facilitator to Event**: One-to-Many
   - A facilitator can have multiple events
   - Each event has one facilitator

4. **Facilitator to BookingNotification**: One-to-Many
   - A facilitator can have multiple notifications
   - Each notification is for one facilitator

## Database Diagram

```
+-------+       +---------+       +--------+
| User  |------>| Booking |<------| Event  |
+-------+       +---------+       +--------+
                    |                 |
                    |                 |
                    v                 |
            +------------------+      |
            | BookingNotification |<---+
            +------------------+      |
                    ^                 |
                    |                 |
                    |                 |
              +-----------+           |
              |Facilitator|<----------+
              +-----------+
```