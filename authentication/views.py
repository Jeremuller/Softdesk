from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsOwner


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)