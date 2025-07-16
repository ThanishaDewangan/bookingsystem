# Booking System for Sessions & Retreats

A complete booking system for managing sessions and retreats with user authentication, event management, booking functionality, and CRM integration.

## Features

- **User Authentication**
  - JWT-based authentication
  - Google OAuth integration
  - User registration and login

- **Event Management**
  - Browse available sessions and retreats
  - View event details and facilitator information
  - Check available spots

- **Booking System**
  - Book sessions and retreats
  - View past and upcoming bookings
  - Cancel bookings

- **Facilitator Integration**
  - Secure CRM notification system
  - View registered users
  - Modify session details
  - Cancel sessions

## Project Structure

```
booking_system/
├── main_app/                  # Main Flask application
│   ├── app.py                 # Main application code
│   ├── static/                # Static assets
│   │   └── css/               # CSS stylesheets
│   └── templates/             # HTML templates
│       ├── index.html         # Landing page
│       ├── login.html         # Login/register page
│       └── dashboard.html     # User dashboard
├── crm_app/                   # CRM Flask application
│   ├── crm_app.py             # CRM notification service
│   └── templates/             # CRM HTML templates
│       └── dashboard.html     # Facilitator dashboard
├── frontend/                  # Frontend assets
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables
├── init_db.py                 # Database initialization script
├── run.py                     # Script to run both applications
├── start.bat                  # Windows batch file to start the system
├── API_DOCUMENTATION.md       # API documentation
├── DATABASE_SCHEMA.md         # Database schema documentation
├── PROJECT_SUMMARY.md         # Project overview and summary
├── SECURITY_DOCUMENTATION.md  # Security practices documentation
└── PAYMENT_ROADMAP.md         # Payment integration roadmap
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/booking-system.git
   cd booking-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Update the `.env` file with your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   CRM_BEARER_TOKEN=secure-bearer-token-123
   CRM_ENDPOINT=http://localhost:5001/notify
   DATABASE_URL=sqlite:///booking_system.db
   ```

### Running the Application

#### Option 1: Using the start.bat file (Windows)

1. Simply run the start.bat file:
   ```
   start.bat
   ```
   This will set up the environment, install dependencies, initialize the database, and start both applications.

#### Option 2: Using the run.py script

1. Initialize the database:
   ```
   python init_db.py
   ```

2. Run both applications using the run.py script:
   ```
   python run.py
   ```

#### Option 3: Manual startup

1. Initialize the database:
   ```
   python init_db.py
   ```

2. Start the main application (in one terminal):
   ```
   cd main_app
   python app.py
   ```

3. Start the CRM application (in another terminal):
   ```
   cd crm_app
   python crm_app.py
   ```

4. Access the applications:
   - Main app: http://localhost:5000
   - CRM app: http://localhost:5001

## User Guide

### User Authentication

1. Register a new account or login with existing credentials
2. Alternatively, use Google OAuth for quick login

### Browsing Events

1. After login, you'll see available events on the dashboard
2. View event details including date, time, facilitator, and available spots

### Booking a Session

1. Click "Book Now" on any available event
2. Your booking will be confirmed and added to "My Bookings"
3. The facilitator will be notified through the CRM system

### Managing Bookings

1. View all your bookings under the "My Bookings" tab
2. Cancel any upcoming booking if needed

### Facilitator Access

1. Access the CRM dashboard at http://localhost:5001
2. View all booking notifications
3. Manage events and registered users
4. Update or cancel sessions as needed

## API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API endpoints and usage.

## Database Schema

See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for database design and relationships.

## Security Documentation

See [SECURITY_DOCUMENTATION.md](SECURITY_DOCUMENTATION.md) for security practices implemented.

## Payment Integration Roadmap

See [PAYMENT_ROADMAP.md](PAYMENT_ROADMAP.md) for the plan to add payment processing.

## Project Summary

See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for an overview of the implementation.

## 🎯 Bonus Features Completed

### ✅ Payment Integration Roadmap
- Comprehensive 6-phase payment integration plan
- Stripe integration strategy
- Refund system design
- Security considerations
- Timeline and budget planning

### ✅ Security Documentation
- JWT authentication implementation
- Bearer token security
- OAuth integration details
- Input validation practices
- Production security recommendations

### ✅ Deployment Ready
- Railway deployment configuration
- Render deployment alternative
- Production environment setup
- Environment variables configuration
- Health checks and monitoring

### ✅ Complete Documentation
- API documentation with examples
- Database schema with relationships
- Security practices documentation
- Payment integration roadmap
- Deployment guide
- Project structure overview

## 🚀 Deployment URLs

### Free Hosting Options
- **Railway**: [Deploy Now](https://railway.app) (Recommended)
- **Render**: [Deploy Now](https://render.com) (Alternative)

### Sample Deployment
```
Main App: https://booking-system-production.up.railway.app
CRM Dashboard: https://booking-system-crm.up.railway.app
```

## 📊 Project Completion Status

| Requirement | Status | Details |
|-------------|--------|---------|
| User Authentication | ✅ Complete | JWT + Google OAuth |
| Event Browsing | ✅ Complete | Real-time data |
| Booking System | ✅ Complete | Full CRUD operations |
| CRM Integration | ✅ Complete | Real-time notifications |
| API Documentation | ✅ Complete | Comprehensive docs |
| Database Models | ✅ Complete | Proper relationships |
| Security Practices | ✅ Complete | Production-ready |
| **Bonus: Payment Roadmap** | ✅ Complete | 6-phase plan |
| **Bonus: Security Docs** | ✅ Complete | Detailed practices |
| **Bonus: Deployment Ready** | ✅ Complete | Multiple options |
| **Bonus: Documentation** | ✅ Complete | Professional grade |

## License

MIT License