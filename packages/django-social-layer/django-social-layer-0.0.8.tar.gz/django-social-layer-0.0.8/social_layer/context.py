from social_layer.models import Notification

def social_layer_data(request):
    if request.user.is_authenticated:
        notifs = Notification.objects.filter(to=request.user).count()
    else:
        notifs = None
    data = {
        'notif_count': notifs,
        }
    return data

