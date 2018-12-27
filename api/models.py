from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
    date = models.DateField()
    explorer = models.CharField(max_length=50)
