from rest_framework import serializers
from .models import Story
from Account.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'username', 'image',]



class StorySerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    author = CustomUserSerializer(read_only=True)


    class Meta:
        model = Story
        fields = ['id', 'author', 'caption', 'location', 'created_at', 'updated_at', 'image']