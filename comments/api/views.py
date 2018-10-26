from rest_framework.viewsets import ModelViewSet
from comments.models import Comment
from .serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from .permissions import UserIsOnwer
from rest_framework import permissions

class CommentModelViewSet(ModelViewSet)  :

    serializer_class = CommentSerializer
    permission_classes = [UserIsOnwer,permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) :
        return Comment.objects.filter(deleted = False)

    def create(self,request,*args,**kwargs) :
        user = request.user
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid() :
            serializer.save(initiator = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
