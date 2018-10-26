from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer
from events.models import Event
from rest_framework.response import Response
from rest_framework import status


class EventModelViewSet(ModelViewSet) :

    serializer_class = EventSerializer

    def get_queryset(self) :
        return Event.objects.all()

    def create(self,request,*args,**kwargs) :
        user = request.user
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid() :
            serializer.save(initiator = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
