from .models import sysNotification
def notification_data(request):
    myId = request.session.get('id')
    if myId:
        unread_count = sysNotification.objects.filter(user_id=myId, is_read=False).count()
        latest_notifications = sysNotification.objects.filter(user_id=myId, is_read=False).order_by('-created_at')[:4]
        return {
            'notification_count': unread_count,
            'latest_notifications': latest_notifications,
        }
    return {'notification_count': 0, 'latest_notifications': []}