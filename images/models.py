from django.db import models
from users.models import User
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from events.models import Event

class Tag(models.Model) :

    content = models.CharField(max_length = 100,unique = True)

    def __str__(self) :
        return self.content

    def get_images(self) :
        return self.image_set.filter(deleted = False)

    def get_images_number(self) :
        return self.get_images().count()

    @property
    def img_num(self) :
        return self.get_images_number()


class ImageManager(models.Manager) :

    def all(self) :
        return self.filter(deleted = False)

    def get_deleted(self) :
        return self.filter(deleted = True)

class Image(models.Model) :

    deleted = models.BooleanField(default = False)
    height = models.IntegerField(default = 0)
    width  = models.IntegerField(default = 0)
    image = models.ImageField(width_field = "width",height_field = "height",upload_to='uploades/')
    tags = models.ManyToManyField(Tag)
    thumbnail = models.ImageField(upload_to='thumbnails/',default = None)
    objects = ImageManager()

    @property
    def comments(self) :
        img_contnet_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type = img_contnet_type,object_id = self.id,deleted = False)

    @property
    def comments_num(self) :
        return self.comments.count()

    @property
    def uploader(self) :
        img_content_type = ContentType.objects.get_for_model(self.__class__)
        qs =  Event.objects.filter(
            event_type = 'upload',
            object_id = self.id,
            content_type = img_content_type
        )
        if qs.exists() :
            return qs.first().initiator
        else :
            return self.__class__.objects.none()


    @property
    def uploader_username(self) :
        result = self.uploader
        try :
            assert type(result) == User
            return result.username
        except AssertionError :
            User.objects.first().username

    @property
    def likes(self) :
        img_content_type = ContentType.objects.get_for_model(self.__class__)
        qs = Event.objects.filter(
            event_type = 'like' ,
            content_type = img_content_type,
            object_id = self.id,
        )
        return qs

    @property
    def likes_num(self) :
        return self.likes.count()


    def is_liked_by_user(self,user) :

        img_content_type = ContentType.objects.get_for_model(self.__class__)
        return Event.objects.filter(
            event_type = 'like',
            initiator = user,
            content_type = img_content_type,
            object_id = self.id
        ).exists()


    #this method won't be used directly it's part of other methods
    def get_upload_event(self,user = None) :
        img_content_type = ContentType.objects.get_for_model(self.__class__)
        if not user :
            upload_event_qs = Event.objects.filter(
                event_type = 'upload',
                content_type = img_content_type,
                object_id = self.id
            )
        else :
            upload_event_qs = Event.objects.filter(
                event_type = 'upload',
                content_type = img_content_type,
                object_id = self.id,
                initiator = user
            )
        return upload_event_qs # this will be a queryset


    def get_upload_time(self) :
        return self.get_upload_event().first().timestamp


    def is_owner(self,user) :
        upload_event_qs = self.get_upload_event(user)
        return True if upload_event_qs else False


    def __str__(self) :
        return self.image.url
