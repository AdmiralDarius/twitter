from django.contrib import admin

from .models import TwitterUser,Twit,SavedRequests

admin.site.register(TwitterUser)
admin.site.register(Twit)
admin.site.register(SavedRequests)