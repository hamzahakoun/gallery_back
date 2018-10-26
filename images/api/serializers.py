from rest_framework import serializers
from images.models import Image, User, Tag
from .utils import *
from comments.api.serializers import CommentSerializer
from events.api.serializers import EventSerializer
from users.api.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Tag
        fields = ['content','id','img_num']






class ImageUpdateSerializer(serializers.ModelSerializer) :


    tags = TagSerializer(many = True,read_only = True)
    tags_list = serializers.CharField(max_length = 1000,write_only = True)

    class Meta :
        model = Image
        fields = ['deleted','tags','tags_list']

    def update(self,instance,validated_data) :
        # if the used wants to deleted the image
        # then remove all links between this image and all assocciated tags
        # then set deleted to True

        if validated_data.get('deleted') :
            instance.tags.clear()
            instance.deleted = True
            instance.save()
            return instance

        else :
            print('else else else')
            # if the user wants to add new tags on image
            # then create none existing tags and link all tags to this image
            tags = validated_data.get('tags_list').split('#')
            create_none_existing_tags(tags)

            for t in tags :
                tag_obj = Tag.objects.get(content = t)
                instance.tags.add(tag_obj)
            instance.save()
            return instance


class ImageSerializer(serializers.ModelSerializer) :

    tags_list = serializers.CharField(max_length = 1000,write_only = True)
    tags = TagSerializer(many = True,read_only = True)
    comments = CommentSerializer(many = True,read_only = True)
    comments_num = serializers.IntegerField(read_only = True)
    width = serializers.IntegerField(read_only = True)
    height = serializers.IntegerField(read_only = True)
    likes = EventSerializer(read_only = True,many = True)
    likes_num = serializers.IntegerField(read_only = True)
    uploader = UserSerializer(read_only = True)
    thumbnail = serializers.ImageField(read_only = True)
    url = serializers.ImageField(source = 'image')
    is_liked_by_user = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta :
        model = Image
        fields = [
            'id',
            'tags_list',
            'tags',
            'comments',
            'comments_num',
            'deleted',
            'width',
            'height',
            'likes',
            'likes_num',
            'uploader',
            'thumbnail',
            'url',
            'is_liked_by_user',
            'timestamp' ,
            'is_owner' ,
        ]


    def get_is_owner(self,obj) :
        user = self.context['request'].user
        return obj.is_owner(user)

    def get_is_liked_by_user(self,obj) :
        user = self.context['request'].user
        return obj.is_liked_by_user(user)

    def get_timestamp(self,obj) :
        return obj.get_upload_time()


    def create(self,validated_date)  :
        img_obj = validated_date.get('image')
        tags = validated_date.get('tags_list').split('#')
        initiator = validated_date.get('initiator')
        img = upload_img(img_obj,tags,initiator)
        return img




    #deleted the like object assocciated with this image object if any
