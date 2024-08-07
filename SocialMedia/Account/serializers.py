from rest_framework import serializers
from .models import *
from .validators import validate_password_complexity,validate_email,validate_username
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from django.contrib.auth.models import User
from phonenumbers import parse,is_valid_number,NumberParseException


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password_complexity])
    email = serializers.EmailField(required=True, validators=[validate_email])
    username = serializers.CharField(required=True, validators=[validate_username])
    image=serializers.ImageField(max_length=None,use_url=True,required=False)
    # follower_count = serializers.SerializerMethodField()
    # folllowing_count = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','password','image','follower_count','following_count','name','dob','location','phone_number']

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


class BioUpdateSerializer(serializers.ModelSerializer):
    def validate_phone_number(self, value):
        try:
            parsed_number = parse(value, None) 
            if not is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number")
        except NumberParseException:
            raise serializers.ValidationError("Invalid phone number format")
        return value
    class Meta:
        model = CustomUser
        fields = ['name','dob','phone_number','location','image']


class SearchSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'image', 'is_following']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user.following_profiles.filter(id=obj.id).exists()
        return False

