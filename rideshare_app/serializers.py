from rest_framework import serializers, validators
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from rideshare_app.models import CustomUser, Ride


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="This email is already in use.")]
    )
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name', 'password','is_driver')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegistrationSerializer, self).create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"

