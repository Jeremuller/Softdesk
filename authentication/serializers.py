from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'age', 'can_data_be_shared', 'can_be_contacted']
        read_only_fields = ['id', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }