from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'crm-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_notifications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CRM Models
class BookingNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    event_title = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    facilitator_id = db.Column(db.Integer, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)

def validate_bearer_token(token):
    """Validate the Bearer token"""
    expected_token = os.getenv('CRM_BEARER_TOKEN', 'secure-bearer-token-123')
    return token == f'Bearer {expected_token}'

@app.route('/api/notifications', methods=['GET'])
def get_api_notifications():
    """Endpoint to get all notifications (API version)"""
    notifications = BookingNotification.query.order_by(BookingNotification.received_at.desc()).all()
    return jsonify([{
        'id': n.id,
        'booking_id': n.booking_id,
        'user_name': n.user_name,
        'user_email': n.user_email,
        'event_title': n.event_title,
        'event_date': n.event_date.isoformat(),
        'facilitator_id': n.facilitator_id,
        'received_at': n.received_at.isoformat(),
        'processed': n.processed
    } for n in notifications])

@app.route('/notify', methods=['POST'])
def receive_booking_notification():
    """Endpoint to receive booking notifications from main app"""
    
    # Validate Authorization header (from header or form)
    auth_header = request.headers.get('Authorization')
    auth_form = request.form.get('authorization')
    
    if auth_header and validate_bearer_token(auth_header):
        # Valid header auth
        pass
    elif auth_form and validate_bearer_token(auth_form):
        # Valid form auth
        pass
    else:
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid or missing Bearer token'
        }), 401
    
    # Validate Content-Type (allow both JSON and form data)
    if not (request.content_type.startswith('application/json') or 
            request.content_type.startswith('application/x-www-form-urlencoded') or
            request.content_type.startswith('multipart/form-data')):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Content-Type must be application/json or form data'
        }), 400
    
    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            # Try to get data from form
            notification_str = request.form.get('notification')
            if notification_str:
                data = json.loads(notification_str)
            else:
                data = request.get_json()
        
        # Validate required fields
        required_fields = ['booking_id', 'user', 'event', 'facilitator_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Validate nested user fields
        user_fields = ['id', 'name', 'email']
        for field in user_fields:
            if field not in data['user']:
                return jsonify({
                    'error': 'Bad Request',
                    'message': f'Missing required user field: {field}'
                }), 400
        
        # Validate nested event fields
        event_fields = ['id', 'title', 'date_time']
        for field in event_fields:
            if field not in data['event']:
                return jsonify({
                    'error': 'Bad Request',
                    'message': f'Missing required event field: {field}'
                }), 400
        
        # Parse event date
        try:
            event_date = datetime.fromisoformat(data['event']['date_time'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid date_time format'
            }), 400
        
        # Store notification in database
        notification = BookingNotification(
            booking_id=data['booking_id'],
            user_name=data['user']['name'],
            user_email=data['user']['email'],
            event_title=data['event']['title'],
            event_date=event_date,
            facilitator_id=data['facilitator_id']
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Log the notification
        print(f"[{datetime.utcnow()}] New booking notification:")
        print(f"  Booking ID: {data['booking_id']}")
        print(f"  User: {data['user']['name']} ({data['user']['email']})")
        print(f"  Event: {data['event']['title']}")
        print(f"  Facilitator ID: {data['facilitator_id']}")
        
        # Create notification object for the dashboard
        notification_data = {
            'id': notification.id,
            'booking_id': data['booking_id'],
            'user_name': data['user']['name'],
            'user_email': data['user']['email'],
            'event_title': data['event']['title'],
            'event_date': data['event']['date_time'],
            'facilitator_id': data['facilitator_id'],
            'received_at': datetime.utcnow().isoformat(),
            'processed': False
        }
        
        # Return HTML with JavaScript to update the dashboard directly
        html_response = f"""
        <html>
        <body>
            <script>
            try {{                
                // Add notification to parent window if available
                if (window.parent && window.parent.addNotification) {{                    
                    window.parent.addNotification({json.dumps(notification_data)});
                }}
                
                // Also try to add to opener window
                if (window.opener && window.opener.addNotification) {{                    
                    window.opener.addNotification({json.dumps(notification_data)});
                }}
            }} catch(e) {{                
                console.error('Error sending notification to parent/opener:', e);
            }}
            </script>
            <p>Notification received</p>
        </body>
        </html>
        """
        
        # Check if client wants JSON
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                'status': 'success',
                'message': 'Booking notification received and processed',
                'notification_id': notification.id
            }), 200
        
        # Otherwise return HTML with embedded script
        response = make_response(html_response)
        response.headers['Content-Type'] = 'text/html'
        return response
        
    except Exception as e:
        print(f"Error processing notification: {str(e)}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to process booking notification'
        }), 500

@app.route('/notifications', methods=['GET'])
def get_notifications():
    """Get all booking notifications (for CRM dashboard)"""
    
    # Simple authentication check
    auth_header = request.headers.get('Authorization')
    if not auth_header or not validate_bearer_token(auth_header):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid or missing Bearer token'
        }), 401
    
    notifications = BookingNotification.query.order_by(BookingNotification.received_at.desc()).all()
    
    return jsonify([{
        'id': notification.id,
        'booking_id': notification.booking_id,
        'user_name': notification.user_name,
        'user_email': notification.user_email,
        'event_title': notification.event_title,
        'event_date': notification.event_date.isoformat(),
        'facilitator_id': notification.facilitator_id,
        'received_at': notification.received_at.isoformat(),
        'processed': notification.processed
    } for notification in notifications])

@app.route('/notifications/<int:notification_id>/process', methods=['POST'])
def mark_notification_processed(notification_id):
    """Mark a notification as processed"""
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not validate_bearer_token(auth_header):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid or missing Bearer token'
        }), 401
    
    notification = BookingNotification.query.get_or_404(notification_id)
    notification.processed = True
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Notification marked as processed'
    })

@app.route('/', methods=['GET'])
def dashboard():
    """Render the facilitator dashboard"""
    return render_template('dashboard.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'CRM Notification Service',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method Not Allowed',
        'message': 'The method is not allowed for the requested URL'
    }), 405

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)