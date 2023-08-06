from django.contrib import admin

# Register your models here.
from social_layer.models import *


admin.site.register(SocialProfile)
admin.site.register(Comment)
admin.site.register(CommentSection)
admin.site.register(Notification)
admin.site.register(LikeComment)
