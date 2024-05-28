from django.shortcuts import render
from rest_framework import generics
from .serializers import StorySerializer
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from .models import Story
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.



class StoryListCreateApiView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        now = timezone.now()
        return Story.objects.filter(author__in=following_users, created_at__gte=now - timedelta(hours=24))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'status': 1, 'stories': serializer.data}, status=status.HTTP_200_OK)


class StoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    



class DeleteStory(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk,*args,**kwargs):
        try:
            story = Story.objects.get(pk=pk)
            if story.author==request.user:
                story.delete()
                return Response({'status':1,'message':'story deleted successfully.'},status=status.HTTP_200_OK)
            else:
                return Response({'status':0,'error':'you do not have permission to delete this story.'},status=status.HTTP_403_FORBIDDEN)
        except Story.DoesNotExist:
            return Response({'status':0,'error':'story not found'},status=status.HTTP_404_NOT_FOUND)