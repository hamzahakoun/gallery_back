from django.db import models
from users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Event(models.Model) :

    event_type = models.CharField(max_length = 50)
    timestamp = models.DateTimeField(auto_now = True, auto_now_add = False)
    initiator = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    def __str__(self) :
        return self.event_type
