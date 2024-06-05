from rest_framework import serializers
from .models import Message
from Account.models import CustomUser






class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message','image']

class MessageListSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    class Meta:
        model = Message
        fields = ['sender_username','receiver_username','timestamp','message','image']  

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('image'):
            representation['image'] = representation['image'].replace('http://127.0.0.1:8000', '')
        return representation


