from rest_framework import serializers
from .models import *
from .validators import validate_password_complexity,validate_email,validate_username
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password_complexity])
    email = serializers.EmailField(required=True, validators=[validate_email])
    username = serializers.CharField(required=True, validators=[validate_username])
    image=serializers.ImageField(max_length=None,use_url=True,required=False)
    # follower_count = serializers.SerializerMethodField()
    # folllowing_count = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','password','image','follower_count','following_count']

    def create(self, validated_data):
        user=CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        if 'image' in validated_data:
            user.image = validated_data['image']
        user.save()
        return user
    def get_follower_count(self, obj):
        return obj.follower.count() 
    def get_following_count(self,obj):
        return obj.following.count()
    
    
    
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["username"] = user.username
        data["email"] = user.email
        return data

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields=[]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'image', 'is_active', 'is_admin')


class FollowerSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer(many=True)  

    class Meta:
        model = CustomUser
        fields = ('follower',)


class FollowingSerializer(serializers.ModelSerializer):
    following = CustomUserSerializer(many=True) 

    class Meta:
        model = CustomUser
        fields = ('following',)


