from rest_framework import serializers
from .models import Post,Like,Comment
from Account.models import CustomUser

class PostListSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='id')
    like_count=serializers.SerializerMethodField() 
    author=serializers.SerializerMethodField() 
    is_liked = serializers.SerializerMethodField()
    comments_count=serializers.SerializerMethodField() 
    class Meta:
        model = Post
        fields =['post_id','author','caption','location','created_at','image','like_count','is_liked','comments_count']
        
    def get_author(self, obj):
        profile_image_url = obj.author.image.url if obj.author.image else ''
        return {'author_id':obj.author.id,'author_name':obj.author.username,'profile_image':profile_image_url}
       
    def get_like_count(self, obj):
        return obj.liked_by.count()
    
    def get_is_liked(self, obj):       
        request_user = self.context['request'].user
        print(request_user)  
        if request_user:
            return obj.liked_by.filter(id=request_user.id).exists()
        return False
    
    
    def get_comments_count(self, obj):
        return obj.comments.count()
        




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'image']




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