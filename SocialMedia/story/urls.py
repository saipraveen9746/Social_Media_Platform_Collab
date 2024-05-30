from django.urls import path
from .views import StoryListCreateApiView,StoryDetailAPIView,DeleteStory,UserStoryList




urlpatterns = [
    path('stories/',StoryListCreateApiView.as_view(),name='story-list-create'),
    path('story/<int:pk>/',StoryDetailAPIView.as_view(),name='story-detail'),
    path('storydelete/<int:pk>/',DeleteStory.as_view(),name='delete-story'),
    path('userstoryview/',UserStoryList.as_view(),name='user-story')

]