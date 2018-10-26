from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from events.models import Event
from users.models import User

class Comment(models.Model) :

    deleted = models.BooleanField(default = False)
    content = models.TextField(max_length = 1000)
    is_parent = models.BooleanField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,default = 6)
    object_id = models.PositiveIntegerField(default = 1)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) :
        return self.content

    @property
    def commentor(self) :
        comment_content_type = ContentType.objects.get_for_model(self.__class__)
        comment_qs = Event.objects.filter(
            content_type = comment_content_type ,
            object_id = self.id ,
            event_type = 'comment'
        )
        if comment_qs.exists() :
            return comment_qs.first().initiator
        else :
            return self.__class__.objects.none()

    @property
    def commentor_username(self) :
        result = self.commentor
        try :
            assert type(result) == User
            return result.username
        except AssertionError :
            return User.objects.first().username

    @property
    def timestamp(self) :
        comment_content_type = ContentType.objects.get_for_model(self.__class__)
        comment_qs = Event.objects.filter(
            content_type = comment_content_type ,
            object_id = self.id ,
            event_type = 'comment'
        )
        if comment_qs.exists() :
            return comment_qs.first().timestamp
        else :
            return 0

    def is_user_owner(self,user_object) :
        return self.commentor == user_object
