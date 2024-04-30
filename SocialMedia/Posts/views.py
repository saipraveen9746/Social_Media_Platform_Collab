from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

from rest_framework.permissions import IsAuthenticated
# Create your views here.
class AuthenticatedUserPostListView(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            appointments = Post.objects.filter(author=request.user)
            
            serializer = AuthenticatedUserPostListSerializer(appointments, many=True)
            
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"status":0,"error":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)



class CreatePostView(APIView):
    serializer_class = PostcreateSerializer
    permission_classes=[IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = PostcreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response({"status": 1, "message": "Post created successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": 0, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)

            if post.author == request.user:  # Permission check
                post.delete()  # Delete the comment
                return Response({"status": 1,"message": "post deleted successfully."}, status=status.HTTP_200_OK)
            
            else:
                # User is not authorized to delete the comment
                return Response({"status": 0,"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

        except Comment.DoesNotExist:
            # If the comment does not exist
            return Response({"status": 0,"error": "post not found."}, status=status.HTTP_404_NOT_FOUND)


        
        
        
class Like_dislikePostView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can like posts

    def post(self, request):
        try:
            serializer = Like_dislikePostSerializer(data=request.data)       
            if serializer.is_valid():
                post = serializer.validated_data['post']
                user = request.user
                existing_like = Like.objects.filter(user=user, post=post).first()         
                if existing_like:
                    # If the user already likes the post, delete the like (dislike)
                    existing_like.delete()
                    return Response({"status": 1,"message": "Post disliked successfully."}, status=status.HTTP_200_OK)
                else:
                    # If the user doesn't like the post, create a new like
                    Like.objects.create(user=user, post=post)
                    return Response({"status": 1,"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"status": 0,"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
        
        
class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = CommentCreateSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"status": 1,"message": "Comment created successfully.","data": serializer.data}, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"status": 0,"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        
        
        
class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=pk)

            if comment.user == request.user or comment.post.author == request.user:  # Permission check
                comment.delete()  # Delete the comment
                return Response({"status": 1,"message": "Comment deleted successfully."}, status=status.HTTP_200_OK)
            
            else:
                # User is not authorized to delete the comment
                return Response({"status": 0,"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        except Comment.DoesNotExist:
            # If the comment does not exist
            return Response({"status": 0,"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
class ListCommentsForPostView(APIView):
    permission_classes = [IsAuthenticated]  # Adjust as needed (e.g., require authentication)

    def get(self, request, post_id, *args, **kwargs):
        try:
            comments = Comment.objects.filter(post_id=post_id).order_by('created_at')  # Order by creation date
            
            serializer = CommentListSerializer(comments,many=True,context={'request': request},)
            return Response({"status": 1,"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
        