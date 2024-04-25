from rest_framework import serializers
from .models import *
from .validators import validate_password_complexity,validate_email,validate_username


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password_complexity])
    email = serializers.EmailField(required=True, validators=[validate_email])
    username = serializers.CharField(required=True, validators=[validate_username])
    image=serializers.ImageField(max_length=None,use_url=True,required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email','password','image']

    def create(self, validated_data):
        user=CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        if 'image' in validated_data:
            user.image = validated_data['image']
        user.save()
        return user