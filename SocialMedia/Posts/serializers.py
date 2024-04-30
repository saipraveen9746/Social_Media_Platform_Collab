from rest_framework import serializers
from .models import Post,Like,Comment

class AuthenticatedUserPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields ='__all__'
        

class PostcreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['caption', 'location', 'image']
        read_only_fields = ['author', 'created_at',]
        
        
        
class Like_dislikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post'] 
        
        
        
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'content']
        
        
class CommentListSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    deletable = serializers.SerializerMethodField() 
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at','deletable']
        
    def get_user(self, obj):
        profile_image_url = obj.user.image.url if obj.user.image else ''
        return {'user_id':obj.user.id,'user_name':obj.user.username,'profile_image':profile_image_url}
    
    def get_deletable(self, obj):
        # Check if the comment is created by the authenticated user or if they are the post owner
        request_user = self.context['request'].user
        print(request_user)# Get the authenticated user
        return True if obj.user == request_user or obj.post.author == request_user else False