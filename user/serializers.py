from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Property
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User Model Serializer
    """
    password = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'address', 'state']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer class for property model
    """
    class Meta:
        model = Property
        fields = ['seller', 'title', 'description', 'location', 'state', 'sale_type', 'price',
                  'bedrooms', 'bathroom', 'home_type']
