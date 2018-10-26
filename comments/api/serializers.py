from rest_framework import serializers
from comments.models import Comment
from images.api.utils import create_comment
from users.api.serializers import UserSerializer
from django.contrib.contenttypes.models import ContentType


class CommentSerializer(serializers.ModelSerializer) :

    commentor = UserSerializer(read_only = True)
    timestamp = serializers.DateTimeField(read_only = True)
    content_type = serializers.CharField() ;

    class Meta :
        model = Comment
        fields = '__all__'

    def create(self,validated_data) :
        content = validated_data.get('content')
        is_parent = validated_data.get('is_parent')
        ct = validated_data.get('content_type')
        content_type = ContentType.objects.get(model = ct)
        object_id = validated_data.get('object_id')
        initiator = validated_data.get('initiator')
        comment = create_comment(content,is_parent,content_type,object_id,initiator)
        return comment
