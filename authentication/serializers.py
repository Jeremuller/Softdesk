from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'age', 'can_data_be_shared', 'can_be_contacted']