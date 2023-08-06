
from importlib import import_module
from social_layer.models import SocialProfile, SocialProfilePhoto

def get_social_profile_byuser(user):
    """ returns a SocialProfile object given an user """
    sprofile = SocialProfile.objects.filter(user=user).first()
    if not sprofile:
        sprofile = SocialProfile.objects.create(user=user)
    return sprofile

def get_social_profile(request):
    """ Returns the social profile of the user """
    if request.user.is_authenticated:
        sprofile = get_social_profile_byuser(request.user) 
        if not sprofile.ip:
            sprofile.ip = (request.META.get('HTTP_X_FORWARDED_FOR', None)
                           or request.META.get('REMOTE_ADDR', None))
            sprofile.save()
        return sprofile
    return None

def execute_string(function_string, *args, **kwargs):
    """ executes a function given it name as a string """
    mod_name, func_name = function_string.rsplit('.',1)
    mod = import_module(mod_name)
    func = getattr(mod, func_name)
    result = func(*args, **kwargs)
    return result

    

