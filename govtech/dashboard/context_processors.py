from .models import Notification

def notification_data(request):
    myId = request.session.get('id')

    if myId:
        unread_count = Notification.objects.filter(user_id=myId, is_read=False).count()
        latest_notifications = Notification.objects.filter(user_id=myId, is_read=False).order_by('-created_at')[:4]
        return {
            'user_notification_count': unread_count,
            'user_latest_notifications': latest_notifications,
        }
    return {'user_notification_count': 0, 'user_latest_notifications': [], 'myId': None}
