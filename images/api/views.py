from images.models import Image, Tag
from rest_framework.viewsets import ModelViewSet
from .serializers import ImageSerializer,TagSerializer,ImageUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db.models import Q,Count
from django.contrib.contenttypes.models import ContentType
from events.models import Event
from .permissions import IsUserOwnerOrReadOnly

###sdfsdfsdfsdfsdfsdfsdfad

def get_images_on_tags(tags_list) :
    q = Q()
    result = Image.objects.none()
    for tag in tags_list :
        q |= Q(content = tag)
    for tag in Tag.objects.filter(q) :
        result = result | tag.get_images() # extend query set (merget two querysets together)
    return result.distinct()



class ImageModelViewSet(ModelViewSet) :

    #serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOwnerOrReadOnly]


    def get_serializer_class(self) :
        if self.action in ('create','list','retrieve') :
            return ImageSerializer
        else :
            return ImageUpdateSerializer

    def get_queryset(self) :

        # get images based on a list of tags
        if self.request.GET.get('tags') :

            exclude = self.request.GET.get('exclude')
            tags_list = self.request.GET.get('tags').split(',')
            if (exclude) :
                return get_images_on_tags(tags_list).exclude(id = exclude).order_by('-id')
            else :
                return get_images_on_tags(tags_list).order_by('-id')
                
        # get all images liked by a user
        elif self.request.GET.get('liked') :
            user = self.request.user
            qs =  user.get_img_likes_events()
            result = [event.content_object for event in qs if not event.content_object.deleted]
            return result

        return Image.objects.filter(deleted = False).order_by('-id')

    def create(self,request,*args,**kwargs) :
        user = request.user
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid() :
            serializer.save(initiator = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    #deleted the like object assocciated with this image object if any
    def perform_destroy(self,instance) :

        content_type = ContentType.objects.get(model = 'image')
        event = Event.objects.filter(
            event_type = 'like' ,
            content_type = content_type,
            object_id = instance.id
        ).first()
        event.delete()


class TagModelViewSet(ModelViewSet) :

    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) :
        # return only tags that have images when searching based on tags
        if self.request.GET.get('exists') :
            qs = Tag.objects.annotate(num = Count('image')).order_by('content')
            return qs.filter(num__gt = 0)

        # when creating new image i need all tags
        return Tag.objects.all()
