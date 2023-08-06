from django.shortcuts import render, redirect

# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from mediautils.utils import handle_upload_file

from social_layer.utils import get_social_profile
from social_layer.models import SocialProfile, SocialProfilePhoto, Comment
from social_layer.utils import execute_string
from social_layer.settings import (SOCIAL_ALT_VIEW_PROFILE,
                                   SOCIAL_ALT_SETUP_PROFILE)

@login_required
def setup_profile(request):
    """ Setup the social profile settings """
    did_exist = SocialProfile.objects.filter(user=request.user).exists()
    sprofile = get_social_profile(request)
    if SOCIAL_ALT_SETUP_PROFILE:
        # pass an alternative function if your app needs
        # this should should None if excpets the normal behavior
        response = execute_string(SOCIAL_ALT_SETUP_PROFILE, request)
        if response:
            return response
    if request.method == "POST":
        sprofile.nick = request.POST.get('nick', '')
        sprofile.phrase = request.POST.get('phrase', '')
        #files = request.FILES.getlist('picture')
        #print('FILES', files)
        
        for upload_file in request.FILES:
            foto = handle_upload_file(file_post=request.FILES[upload_file],
                                        quality=2,
                                        Model=SocialProfilePhoto,
                                        extra_args={'profile': sprofile})
            if foto:
                oldies = SocialProfilePhoto.objects.exclude(pk=foto.pk).filter(profile=sprofile)
                oldies.delete()
        sprofile.save()
        # TODO handle spam optin
        receive_email = bool(request.POST.get('receive_email', ''))
        redir_after = request.COOKIES.get('slogin_next', None)
        if redir_after:
            resp = redirect(redir_after)
            resp.delete_cookie('slogin_next')
            return resp
        else:
            return redirect(sprofile.get_url())
    data = {
        'sprofile': sprofile,
        'did_exist': bool(did_exist),
        }
    return render(request, 'social_profile/setup_profile.html', data)
    
def view_profile(request, pk):
    sprofile = SocialProfile.objects.filter(pk=pk).first()
    if not sprofile:
        raise Http404()
    if SOCIAL_ALT_VIEW_PROFILE:
        # pass an alternative function if your app needs.
        # this should return None if excpets the normal behavior
        response = execute_string(SOCIAL_ALT_VIEW_PROFILE, request, sprofile)
        if response:
            return response
    # aqrui funcao alternativa
    data = {
        'sprofile': sprofile,
        'comments': Comment.objects.filter(author=sprofile)
        }
    # a callable that returns a dict for the social profile view
    if getattr(settings, 'SOCIAL_PROFILE_CONTEXT', None):
        extra = execute_string(settings.SOCIAL_PROFILE_CONTEXT, sprofile)
        data.update(extra)
    return render(request, 'social_profile/profile.html', data)


def social_login(request):
    """ any action that requires a social login must be redirected here. 
    It will redirect the user to the 'social' login page.
    """
    next_url = request.GET.get('next', '/')
    #print(next_url)
    resp = redirect('/'+settings.SOCIAL_VISITOR_LOGIN)
    resp.set_cookie('slogin_next', next_url, expires=360) 
    return resp


def list_profiles(request):
    """ List other people's profiles """
    list_profiles = SocialProfile.objects.all().order_by('?')
    data = {'list_profiles': list_profiles[0:100],}
    return render(request, 'social_profile/list_profiles.html', data)
