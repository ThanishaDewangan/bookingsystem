# Deployment Guide

## Free Deployment Options

### Option 1: Railway (Recommended)
**Free Tier**: 500 hours/month + $5 credit

#### Steps:
1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   ```bash
   # Push your code to GitHub first
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

3. **Configure Railway**
   - Connect GitHub repository
   - Railway will auto-detect Python
   - Set environment variables in Railway dashboard

4. **Environment Variables**
   ```
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-secret
   CRM_BEARER_TOKEN=secure-bearer-token-123
   PORT=8080
   ```

### Option 2: Render
**Free Tier**: 750 hours/month

#### Steps:
1. Create account at [render.com](https://render.com)
2. Connect GitHub repository
3. Configure build settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run_apps.py`

### Option 3: Heroku (Limited Free)
**Note**: Heroku ended free tier, but has low-cost options

## Production Deployment Checklist

### Pre-Deployment
- [ ] Update requirements.txt
- [ ] Set production environment variables
- [ ] Configure production database
- [ ] Test all API endpoints
- [ ] Verify CRM notifications work

### Security Configuration
- [ ] Use HTTPS in production
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Use production secret keys
- [ ] Enable rate limiting

### Database Setup
```python
# For production, use PostgreSQL
import os
if os.getenv('DATABASE_URL'):
    # Production database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    # Development database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking_system.db'
```

### Monitoring Setup
- [ ] Set up error logging
- [ ] Configure health checks
- [ ] Monitor API response times
- [ ] Set up uptime monitoring

## Sample Deployment URLs

### Railway Deployment
```
Main App: https://booking-system-production.up.railway.app
CRM App: https://booking-system-production.up.railway.app:5001
```

### Render Deployment
```
Main App: https://booking-system-abc123.onrender.com
CRM App: https://booking-system-crm-abc123.onrender.com
```

## Post-Deployment Testing

### Test Checklist
1. **User Registration/Login**
   - [ ] Email registration works
   - [ ] Google OAuth works
   - [ ] JWT tokens are valid

2. **Event Booking**
   - [ ] Events load correctly
   - [ ] Booking process works
   - [ ] CRM receives notifications

3. **CRM Dashboard**
   - [ ] Notifications display
   - [ ] Mark processed works
   - [ ] View bookings shows real data

### Performance Testing
```bash
# Test API endpoints
curl -X GET https://your-app.railway.app/api/events
curl -X POST https://your-app.railway.app/api/register
```

## Troubleshooting

### Common Issues
1. **Port Configuration**
   ```python
   # Ensure your app uses the PORT environment variable
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

2. **Database Issues**
   - Initialize database on first deployment
   - Check database connection strings
   - Verify table creation

3. **CORS Errors**
   ```python
   # Configure CORS for production
   from flask_cors import CORS
   CORS(app, origins=['https://your-domain.com'])
   ```

## Maintenance

### Regular Tasks
- [ ] Monitor application logs
- [ ] Check database performance
- [ ] Update dependencies
- [ ] Backup database
- [ ] Review security logs

### Scaling Considerations
- Use Redis for session storage
- Implement database connection pooling
- Add load balancing for high traffic
- Consider CDN for static assets