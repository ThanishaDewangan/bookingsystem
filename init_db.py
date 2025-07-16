import os
import sys
from datetime import datetime, timedelta

# Add the project directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the app and models from main_app
from main_app.app import app, db, User, Facilitator, Event, Booking
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if Facilitator.query.first():
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Initializing database with sample data...")
        
        # Create facilitators
        facilitators = [
            Facilitator(name='Dr. Sarah Johnson', email='sarah@example.com', specialization='Mindfulness & Meditation'),
            Facilitator(name='Mike Chen', email='mike@example.com', specialization='Yoga & Wellness'),
            Facilitator(name='Emma Rodriguez', email='emma@example.com', specialization='Life Coaching')
        ]
        
        for facilitator in facilitators:
            db.session.add(facilitator)
        
        db.session.commit()
        print(f"Created {len(facilitators)} facilitators")
        
        # Create events
        events = [
            Event(
                title='Morning Meditation Session', 
                description='Start your day with mindfulness and clarity. This guided meditation session will help you center yourself and prepare for a productive day.',
                event_type='session', 
                date_time=datetime.now() + timedelta(days=1),
                duration=60, 
                max_participants=15, 
                price=25.0, 
                facilitator_id=1
            ),
            Event(
                title='Weekend Yoga Retreat', 
                description='Escape the city for a rejuvenating 2-day yoga retreat in nature. All levels welcome.',
                event_type='retreat', 
                date_time=datetime.now() + timedelta(days=7),
                duration=2880, 
                max_participants=8, 
                price=150.0, 
                facilitator_id=2
            ),
            Event(
                title='Life Coaching Workshop', 
                description='Discover your potential and set actionable goals in this transformative workshop.',
                event_type='session', 
                date_time=datetime.now() + timedelta(days=3),
                duration=120, 
                max_participants=12, 
                price=50.0, 
                facilitator_id=3
            ),
            Event(
                title='Evening Relaxation Session', 
                description='Wind down after a long day with this calming session focused on relaxation techniques.',
                event_type='session', 
                date_time=datetime.now() + timedelta(days=2),
                duration=45, 
                max_participants=20, 
                price=20.0, 
                facilitator_id=1
            ),
            Event(
                title='Career Transition Coaching', 
                description='Navigate career changes with confidence through personalized coaching.',
                event_type='session', 
                date_time=datetime.now() + timedelta(days=5),
                duration=90, 
                max_participants=5, 
                price=75.0, 
                facilitator_id=3
            )
        ]
        
        for event in events:
            db.session.add(event)
        
        db.session.commit()
        print(f"Created {len(events)} events")
        
        # Create users
        users = [
            User(
                name='John Doe',
                email='john@example.com',
                password_hash=generate_password_hash('password123')
            ),
            User(
                name='Jane Smith',
                email='jane@example.com',
                password_hash=generate_password_hash('password123')
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"Created {len(users)} users")
        
        # Create some bookings
        bookings = [
            Booking(
                user_id=1,
                event_id=1,
                booking_date=datetime.now() - timedelta(days=1),
                status='confirmed'
            ),
            Booking(
                user_id=1,
                event_id=3,
                booking_date=datetime.now() - timedelta(hours=12),
                status='confirmed'
            ),
            Booking(
                user_id=2,
                event_id=2,
                booking_date=datetime.now() - timedelta(days=2),
                status='confirmed'
            )
        ]
        
        for booking in bookings:
            db.session.add(booking)
        
        db.session.commit()
        print(f"Created {len(bookings)} bookings")
        
        print("Database initialization complete!")

if __name__ == "__main__":
    init_database()