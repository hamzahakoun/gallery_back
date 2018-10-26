from rest_framework.viewsets import ModelViewSet
from users.models import User
from .serializers import UserSerializer

class UserModelViewSet(ModelViewSet) :

    queryset = User.objects.all()
    serializer_class = UserSerializer
