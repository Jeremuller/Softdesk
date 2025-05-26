from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'age', 'can_data_be_shared', 'can_be_contacted']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            age=validated_data.get('age', 18),
            can_data_be_shared=validated_data.get('can_data_be_shared', False),
            can_be_contacted=validated_data.get('can_be_contacted', False)
        )
        return user