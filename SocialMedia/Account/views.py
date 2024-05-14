from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import FollowersSerializer, FollowersSerializer, FollowingSerializer, UserRegistrationSerializer,UserTokenObtainPairSerializer,CustomUserSerializer,FollowerSerializer,BioUpdateSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions,viewsets

# Create your views here.


class RegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 1, "message": "User registered successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": 0, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
        
        
class UserloginView(APIView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Perform any additional logic if needed
                return Response({"status": 1, "data": serializer.validated_data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": 0, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request, *args, **kwargs):     
        try:
            serializer = UserRegistrationSerializer(self.request.user)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"status":0,"data":"Something went wrpppppppong"}, status=status.HTTP_404_NOT_FOUND)





class CreateFollower(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowersSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get("user_id")
            profile_instance = get_object_or_404(CustomUser, id=user_id)

            if profile_instance.follower.filter(id=request.user.id).exists():
                profile_instance.follower.remove(request.user)
                request.user.following.remove(profile_instance)
                return Response({'status':1,'detail': 'Following removed successfully'}, status=status.HTTP_200_OK)
            else:
                profile_instance.follower.add(request.user)
                request.user.following.add(profile_instance)
                return Response({'status':1,'detail': 'Following added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status':0,'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class UserFollowingList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        try:
            following_users = request.user.following.all()
            serializer = UserRegistrationSerializer(following_users,many=True)
            return Response({'status':1,'data':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':0,'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserFollowerList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        try:
            follower_users = request.user.follower.all()
            serializer = UserRegistrationSerializer(follower_users,many=True)
            return Response({'status':1,'data':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':0,'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomUserList(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        if CustomUser.is_admin:
            queryset = queryset.exclude(is_admin=True)
        return queryset
    def list(self,request,*args,**kwargs):
        try:
            queryset=self.get_queryset()
            serializer = self.get_serializer(queryset,many=True)
            return Response({'status':1,'data':serializer.data})
        except CustomUser.DoesNotExist:
            return Response({'status':0,"error":"CustomUser Does not Exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response ({'status':0,"error": "An error occurred"}, status=500)

class FollowersList(generics.ListAPIView):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return CustomUser.objects.get(id=user_id).follower_profiles.all()
    def list(self,request,*args,**kwargs):
        try:
            queryset = self.get_queryset()
            if queryset.exists():
                serializer = self.get_serializer(queryset,many=True)
                return Response({'status':1,'data':serializer.data})
            else:
                return Response ({'status':0,'error':'no followers'})
        except CustomUser.DoesNotExist:
            return Response({'status':0,'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':0,'error':'An error occured:{}'.format (str(e))}, status=500)
    

class FollowingList(generics.ListAPIView):
    serializer_class = FollowingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return CustomUser.objects.get(id=user_id).following_profiles.all()
    def list(self,request,*args,**kwargs):
        try:
            queryset = self.get_queryset()
            if queryset.exists():
                serializer = self.get_serializer(queryset,many=True)
                return Response({'status':1,'data':serializer.data})
            else:
                return Response({'status':0,'error':'no following'})
        except CustomUser.DoesNotExist:
            return Response({'status':0,'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response ({'status':0,'error':'An error occured:{}'.format (str(e))}, status=500)


class UpdateBioView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = BioUpdateSerializer(instance=user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 1, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 0}, status=status.HTTP_400_BAD_REQUEST)



        