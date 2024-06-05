from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .serializers import MessageSerializer,MessageListSerializer,CustomUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,serializers,permissions
from Chat.models import Message
from Account.models import CustomUser
from Chat import models
from django.http import Http404
from rest_framework.exceptions import NotFound




class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        receiver_id = self.kwargs['receiver']
        try:
            messages = models.Message.objects.filter(receiver_id=receiver_id)
            for message in messages:
                message.is_read = True
                message.save()
            return messages
        except models.Message.DoesNotExist:
            raise Http404('Message is not found for this receiver')
    
    def perform_create(self, serializer):
        receiver_id = self.kwargs.get('receiver')
        receiver = get_object_or_404(models.CustomUser, id=receiver_id)
        try:
            serializer.save(sender=self.request.user, receiver=receiver)
        except Exception as e:
            return Response({'status':0,'error':'an error occurred:{}.format(str(e))'},status=500)


class MessageListAPIView(generics.ListCreateAPIView):
    serializer_class =MessageListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            user = self.request.user
            receiver_id = self.kwargs.get('receiver_id')
            queryset= models.Message.objects.filter(sender=user, receiver_id=receiver_id) | \
                      models.Message.objects.filter(sender_id=receiver_id, receiver=user).order_by('-timestamp')
            return queryset
        except Exception as e:
            raise NotFound(detail='Messages not found receiver this user')
    



class MessageSenderListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            current_user = self.request.user 
            queryset=CustomUser.objects.filter(sent_messages__receiver=current_user).distinct()
            return queryset
        except Exception as e:
            return Response({'status':0,'error':'error occured while rertrieving message senders'},status=status.HTTP_404_NOT_FOUND)



