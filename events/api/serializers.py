from rest_framework import serializers
from events.models import Event
from users.api.serializers import UserSerializer
from django.contrib.contenttypes.models import ContentType
from images.api.utils import create_event


class EventSerializer(serializers.ModelSerializer) :

    initiator = UserSerializer(read_only = True)
    content_type = serializers.CharField()


    class Meta :
        model = Event
        fields = [
            'id',
            'event_type',
            'object_id' ,
            'content_type',
            'initiator',

        ]

    def create(self,validated_data) :
        object_id = validated_data.get('object_id')
        ct = validated_data.get('content_type')
        content_type = ContentType.objects.get(model = ct)
        event_type = validated_data.get('event_type')
        initiator = self.context['request'].user
        event = create_event(event_type,initiator,content_type,object_id)
        return event
