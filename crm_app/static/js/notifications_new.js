// Notifications array - start empty, will be populated by real bookings
const mockNotifications = [];

// Function to add a notification
function addNotification(notification) {
    console.log("Adding notification:", notification);
    
    // Check if it's a raw notification from the main app
    if (notification.user && notification.event) {
        // Convert to the format expected by the dashboard
        mockNotifications.push({
            id: Date.now() + Math.floor(Math.random() * 1000),
            booking_id: notification.booking_id,
            user_name: notification.user.name,
            user_email: notification.user.email,
            event_title: notification.event.title,
            event_date: notification.event.date_time,
            facilitator_id: notification.facilitator_id,
            received_at: new Date().toISOString(),
            processed: false,
            action: notification.action || 'booking'
        });
    } else {
        // It's already in the right format
        mockNotifications.push(notification);
    }
    
    updateNotificationDisplay();
}

// Function to update the notification display
function updateNotificationDisplay() {
    // Update stats
    document.getElementById('total-notifications').textContent = mockNotifications.length;
    document.getElementById('pending-notifications').textContent = 
        mockNotifications.filter(n => !n.processed).length;
    document.getElementById('processed-notifications').textContent = 
        mockNotifications.filter(n => n.processed).length;
    
    // Show notifications
    document.getElementById('notifications-loading').style.display = 'none';
    const notificationList = document.getElementById('notification-list');
    notificationList.style.display = 'block';
    
    if (mockNotifications.length === 0) {
        notificationList.innerHTML = '<p>No notifications yet.</p>';
        return;
    }
    
    notificationList.innerHTML = mockNotifications.map(notification => {
        const isBooking = !notification.action || notification.action === 'booking';
        const isCancellation = notification.action === 'cancellation';
        
        return `
        <li class="notification-item">
            <div class="notification-details">
                <strong>${notification.user_name}</strong> 
                ${isBooking ? 'booked' : isCancellation ? 'cancelled booking for' : 'interacted with'} 
                <strong>${notification.event_title}</strong>
                <div>Event Date: ${new Date(notification.event_date).toLocaleString()}</div>
                <div>Received: ${new Date(notification.received_at).toLocaleString()}</div>
                <span class="badge ${notification.processed ? 'badge-processed' : isCancellation ? 'badge-danger' : 'badge-pending'}">
                    ${notification.processed ? 'Processed' : isCancellation ? 'Cancellation' : 'Pending'}
                </span>
            </div>
            <div class="notification-actions">
                ${!notification.processed ? 
                    `<button class="btn btn-sm" onclick="window.processNotification(${notification.id})">
                        Mark Processed
                    </button>` : 
                    ''}
            </div>
        </li>
        `;
    }).join('');
}

// Function to process a notification
async function processNotification(notificationId) {
    console.log('Processing notification:', notificationId);
    
    try {
        const response = await fetch(`/notifications/${notificationId}/process`, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer secure-bearer-token-123'
            }
        });
        
        if (response.ok) {
            // Update local notification
            const notification = mockNotifications.find(n => n.id === notificationId);
            if (notification) {
                notification.processed = true;
                updateNotificationDisplay();
            }
            alert('Notification marked as processed!');
        } else {
            alert('Failed to process notification');
        }
    } catch (error) {
        console.error('Error processing notification:', error);
        alert('Error processing notification');
    }
}

// Function to check localStorage for notifications
function checkLocalStorageNotifications() {
    try {
        const storedNotifications = JSON.parse(localStorage.getItem('crmNotifications') || '[]');
        if (storedNotifications.length > 0) {
            console.log('Found notifications in localStorage:', storedNotifications);
            
            // Add each notification
            storedNotifications.forEach(data => {
                addNotification(data);
            });
            
            // Clear the localStorage
            localStorage.removeItem('crmNotifications');
        }
    } catch (error) {
        console.error('Error checking localStorage notifications:', error);
    }
}

// Function to fetch notifications from the API
async function fetchNotificationsFromAPI() {
    try {
        const response = await fetch('/notifications', {
            headers: {
                'Authorization': 'Bearer secure-bearer-token-123'
            }
        });
        
        if (response.ok) {
            const notifications = await response.json();
            // Clear existing notifications and add new ones
            mockNotifications.length = 0;
            mockNotifications.push(...notifications);
            updateNotificationDisplay();
            console.log('🔄 Fetched', notifications.length, 'notifications from API');
        }
    } catch (error) {
        console.error('Error fetching notifications from API:', error);
    }
}

// Initialize with mock data
document.addEventListener('DOMContentLoaded', function() {
    updateNotificationDisplay();
    
    // Fetch notifications from API immediately
    fetchNotificationsFromAPI();
    
    // Set up interval to fetch notifications from API
    setInterval(fetchNotificationsFromAPI, 3000); // Check every 3 seconds
    
    // Also check localStorage as backup
    checkLocalStorageNotifications();
    setInterval(checkLocalStorageNotifications, 5000);
});

// Export functions and data to global scope
window.updateNotificationDisplay = updateNotificationDisplay;
window.addNotification = addNotification;
window.processNotification = processNotification;
window.checkLocalStorageNotifications = checkLocalStorageNotifications;
window.mockNotifications = mockNotifications;

// Create a global function to receive notifications from the main app
window.receiveNotification = function(data) {
    console.log("Received notification:", data);
    addNotification(data);
};