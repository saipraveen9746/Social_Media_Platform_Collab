from rest_framework import serializers
from .models import Story
from Account.models import CustomUser
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'username', 'image',]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('image'):
            representation['image'] = representation['image'].replace('http://127.0.0.1:8000 ', '')
        return representation


class StorySerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'author', 'caption', 'location', 'created_at', 'updated_at', 'image']

    def create(self, validated_data):
        request = self.context.get('request')
        image = validated_data.get('image', None)
        if image and isinstance(image, InMemoryUploadedFile):
            # Extract the relative path from the file's name
            validated_data['image'] = image.name
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('image'):
            representation['image'] = representation['image'].replace('http://127.0.0.1:8000', '')
        return representation

