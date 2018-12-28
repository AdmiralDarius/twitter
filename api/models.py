from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.conf import settings

"""
#Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user',on_delete=models.DO_NOTHING)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
"""
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class TwitterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)



class Twit(models.Model):
    owner = models.ForeignKey(TwitterUser, on_delete=models.DO_NOTHING)
    date = models.DateField()
    title = models.CharField(max_length=100, default='title')
    body = models.CharField(max_length=300)


class SavedRequests(models.Model):
    ip = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now=True)
    explorer = models.CharField(max_length=50)
    auth = models.BooleanField(default=True)
    def __str__(self):
        return self.ip + repr(self.time) + repr(self.explorer) + repr(self.auth)