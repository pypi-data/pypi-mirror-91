from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from social_layer.models import Notification

@login_required
def view_notifications(request):
    """ List the past notifications """
    list_notif = Notification.objects.filter(to=request.user).order_by('-date_time')
    data = {
        'list_notif': list_notif,
        'has_notif': False,
        }
    response = render(request, 'notifications/view_notifications.html', data)
    list_notif.filter(read=False).update(read=True)
    return response

def get_notifications(request):
    """ Returns a list of unread notifications of logged in user """
    if request.user.is_authenticated:
        notifs = Notification.objects.filter(to=request.user, read=False)
    else:
        notifs = Notification.objects.none()
    return notifs

@staff_member_required
def admin_send_notification(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method == "POST":
        notif = Notification.objects.create(to=user,
                                            text=request.POST.get('text'))
    list_notifs = Notification.objects.filter(to=user).order_by('-id')
    data = {'list_notif': list_notifs,}
    return render(request, 'notifications/admin_send_notification.html', data)
