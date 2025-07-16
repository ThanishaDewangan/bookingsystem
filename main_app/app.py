from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///booking_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# Google OAuth Config
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')

db = SQLAlchemy(app)
jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'message': 'The token has expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'status': 401,
        'sub_status': 43,
        'message': 'Invalid token: ' + str(error)
    }), 401
CORS(app)
oauth = OAuth(app)

# Google OAuth setup
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={
        'scope': 'email profile'
    }
)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    google_id = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Facilitator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(200))
    events = db.relationship('Event', backref='facilitator', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # session or retreat
    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    max_participants = db.Column(db.Integer, default=10)
    price = db.Column(db.Float, default=0.0)
    facilitator_id = db.Column(db.Integer, db.ForeignKey('facilitator.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='event', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled
    notes = db.Column(db.Text)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    user = User(
        email=data['email'],
        name=data['name'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token, 'user': {'id': user.id, 'name': user.name, 'email': user.email}})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token, 'user': {'id': user.id, 'name': user.name, 'email': user.email}})
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/auth/google')
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo', token=token)
        user_info = resp.json()
        
        # Find or create user
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                email=user_info['email'],
                name=user_info.get('name', user_info['email'].split('@')[0]),
                google_id=user_info.get('id')
            )
            db.session.add(user)
            db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(identity=str(user.id))
        
        # Create a response page that stores token in localStorage
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login Successful</title>
            <script>
                localStorage.setItem('access_token', '{access_token}');
                localStorage.setItem('user', JSON.stringify({{
                    id: {user.id},
                    name: "{user.name}",
                    email: "{user.email}"
                }}));
                window.location.href = '/dashboard';
            </script>
        </head>
        <body>
            <p>Login successful! Redirecting...</p>
        </body>
        </html>
        '''
        return html
    except Exception as e:
        print(f"Google OAuth error: {str(e)}")
        return redirect('/login?error=google_auth_failed')

# Events Routes
@app.route('/api/events', methods=['GET'])
@jwt_required()
def get_events():
    events = Event.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_type': event.event_type,
        'date_time': event.date_time.isoformat(),
        'duration': event.duration,
        'max_participants': event.max_participants,
        'price': event.price,
        'facilitator': event.facilitator.name,
        'available_spots': event.max_participants - len(event.bookings)
    } for event in events])

@app.route('/api/events/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_type': event.event_type,
        'date_time': event.date_time.isoformat(),
        'duration': event.duration,
        'max_participants': event.max_participants,
        'price': event.price,
        'facilitator': {
            'id': event.facilitator.id,
            'name': event.facilitator.name,
            'specialization': event.facilitator.specialization
        },
        'available_spots': event.max_participants - len(event.bookings)
    })

# Booking Routes
@app.route('/api/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    event_id = data['event_id']
    
    event = Event.query.get_or_404(event_id)
    
    # Check if event is full
    if len(event.bookings) >= event.max_participants:
        return jsonify({'message': 'Event is fully booked'}), 400
    
    # Check if user already booked this event
    existing_booking = Booking.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing_booking:
        return jsonify({'message': 'Already booked this event'}), 400
    
    booking = Booking(
        user_id=user_id,
        event_id=event_id,
        notes=data.get('notes', '')
    )
    
    db.session.add(booking)
    db.session.commit()
    
    # Notify CRM
    notify_crm(booking)
    
    return jsonify({
        'message': 'Booking confirmed',
        'booking_id': booking.id,
        'event': event.title,
        'date_time': event.date_time.isoformat()
    })

@app.route('/api/my-bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': booking.id,
        'event': {
            'id': booking.event.id,
            'title': booking.event.title,
            'date_time': booking.event.date_time.isoformat(),
            'event_type': booking.event.event_type
        },
        'booking_date': booking.booking_date.isoformat(),
        'status': booking.status,
        'is_upcoming': booking.event.date_time > datetime.utcnow()
    } for booking in bookings])

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first_or_404()
    
    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled successfully'})

# Facilitator Routes (Admin functionality)
@app.route('/api/facilitator/events/<int:facilitator_id>', methods=['GET'])
@jwt_required()
def get_facilitator_events(facilitator_id):
    events = Event.query.filter_by(facilitator_id=facilitator_id).all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'date_time': event.date_time.isoformat(),
        'bookings_count': len(event.bookings),
        'max_participants': event.max_participants,
        'is_active': event.is_active
    } for event in events])

@app.route('/api/facilitator/events/<int:event_id>/bookings', methods=['GET'])
@jwt_required()
def get_event_bookings(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify([{
        'id': booking.id,
        'user': {
            'name': booking.user.name,
            'email': booking.user.email
        },
        'booking_date': booking.booking_date.isoformat(),
        'status': booking.status,
        'notes': booking.notes
    } for booking in event.bookings])

@app.route('/api/facilitator/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.date_time = datetime.fromisoformat(data.get('date_time', event.date_time.isoformat()))
    event.max_participants = data.get('max_participants', event.max_participants)
    event.price = data.get('price', event.price)
    
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/api/facilitator/events/<int:event_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.is_active = False
    
    # Cancel all bookings
    for booking in event.bookings:
        booking.status = 'cancelled'
    
    db.session.commit()
    return jsonify({'message': 'Event cancelled successfully'})

def notify_crm(booking):
    """Notify CRM system about new booking"""
    try:
        payload = {
            'booking_id': booking.id,
            'user': {
                'id': booking.user.id,
                'name': booking.user.name,
                'email': booking.user.email
            },
            'event': {
                'id': booking.event.id,
                'title': booking.event.title,
                'date_time': booking.event.date_time.isoformat()
            },
            'facilitator_id': booking.event.facilitator_id
        }
        
        headers = {
            'Authorization': f'Bearer {os.getenv("CRM_BEARER_TOKEN")}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            os.getenv('CRM_ENDPOINT'),
            json=payload,
            headers=headers,
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"CRM notification failed: {response.status_code}")
            
    except Exception as e:
        print(f"CRM notification error: {str(e)}")

def init_sample_data():
    """Initialize database with sample data"""
    if not Facilitator.query.first():
        facilitators = [
            Facilitator(name='Dr. Sarah Johnson', email='sarah@example.com', specialization='Mindfulness & Meditation'),
            Facilitator(name='Mike Chen', email='mike@example.com', specialization='Yoga & Wellness'),
            Facilitator(name='Emma Rodriguez', email='emma@example.com', specialization='Life Coaching')
        ]
        
        for facilitator in facilitators:
            db.session.add(facilitator)
        
        db.session.commit()
        
        events = [
            Event(title='Morning Meditation Session', description='Start your day with mindfulness', 
                  event_type='session', date_time=datetime.now() + timedelta(days=1),
                  duration=60, max_participants=15, price=25.0, facilitator_id=1),
            Event(title='Weekend Yoga Retreat', description='2-day wellness retreat in nature',
                  event_type='retreat', date_time=datetime.now() + timedelta(days=7),
                  duration=2880, max_participants=8, price=150.0, facilitator_id=2),
            Event(title='Life Coaching Workshop', description='Discover your potential',
                  event_type='session', date_time=datetime.now() + timedelta(days=3),
                  duration=120, max_participants=12, price=50.0, facilitator_id=3)
        ]
        
        for event in events:
            db.session.add(event)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
    app.run(debug=True, port=5000)