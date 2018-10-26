from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser) :

    avatar = models.ImageField()

    def __str__(self) :
        return self.username

    #get all like event for this user (on images only)
    def get_img_likes_events(self) :
        img_content_type = ContentType.objects.get(model = 'image')
        event_model = ContentType.objects.get(model = 'event').model_class()
        qs = event_model.objects.filter(event_type = 'like',content_type=img_content_type,initiator = self)
        return qs
