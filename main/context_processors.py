from main.models import Notification


def notifications_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_notifications = notifications.filter(is_seen=False)
    else:
        notifications = None
        unread_notifications = None
    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications
    }
    return context
