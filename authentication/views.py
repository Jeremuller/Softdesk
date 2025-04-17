from rest_framework.viewsets import ModelViewSet

from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()