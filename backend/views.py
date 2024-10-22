from django.shortcuts import render
from .serializer import Signup, PostSerializer, UserSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Post, Comment
from django.shortcuts import get_object_or_404


#signup view
class SignupViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self,request):
            serializer = Signup(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                response_data= {"id": user.id, **serializer.data}
                return Response(response_data, status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#login view
class LoginViewSet(viewsets.ViewSet):

    @action(detail=False,methods=['post'])
    def login(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
             return Response({"error":"Kindly fill all the fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
             user = User.objects.get(email=email)
        except User.DoesNotExist:
             return Response({"error":"Invalid email or password"}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
             return Response({"error":"Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
             'id': user.id,
             'email': user.email,
             'refresh': str(refresh),
             'access': access_token},
             status=status.HTTP_200_OK) 
    

class SomeSecureView(viewsets.ViewSet): 
     permission_classes = [IsAuthenticated]

     @action(detail=False, method=['get'])
     def secure_data(self,request):
          return Response({"data":"This is secured view!"})
     

# User Home Screen
class HomeViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

    def home(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response({
            "message": "WELCOME", 
            "posts": serializer.data, 
            "user": user.id 
        }, status=status.HTTP_200_OK)


# Create Post View Set
class CreatePostViewSet(viewsets.ViewSet):
     # permission_classes = [IsAuthenticated]

     @action(detail=True, methods=['post'])
     def create_post(self,request, pk=None):
          user = User.objects.get(pk=pk)
          serializer = PostSerializer(data=request.data)

          if serializer.is_valid():
               serializer.save(user=user)
               return Response({"user":user.id,
                                "serializer":serializer.data,
                                },
                                status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

# Single Post View Set 
class SinglePostViewSet(viewsets.ViewSet):
     
     @action(detail=True, method=['Get','Delete','Put'])
     def single_post(self,request, pk=None, post_id=None):
          user = User.objects.get(pk=pk)
          post = Post.objects.get(pk=post_id, user=user)

          if request.method == 'GET':
            serializer = PostSerializer(post)
            return Response({"user":user.id,
                                "post":serializer.data
                                },
                                status=status.HTTP_200_OK)
          
          if request.method == 'PUT':
               update_serializer = PostSerializer(post, data=request.data, partial=True)
               if update_serializer.is_valid():
                    update_serializer.save()
                    return Response({"message":"updated",
                                     "user":user.id,
                                     "post":update_serializer.data},
                               status=status.HTTP_200_OK)

          
          if request.method == 'DELETE':
               post.delete()
               return Response({'message',f'post {post.post_text} deleted successfully'},
                               status=status.HTTP_200_OK)
     

# User Posts
class Profile(viewsets.ViewSet):
     
     @action(detail=True, methods=['Get'])
     def profile(self,request,pk=None):
          user = User.objects.get(pk=pk)
          posts = Post.objects.filter(user=user)
          serializer = PostSerializer(posts, many=True)
          friends = user.friend.count()
          return Response({"user":user.id,
                           "friends":friends,
                           "post":serializer.data,
                           },
                           status=status.HTTP_200_OK)
     

# Search View Set
class SearchViewSet(viewsets.ViewSet):
     
     @action(detail=True, methods=['Post'])
     def search(self,request,pk=None):
          user = User.objects.get(pk=pk)
          first_name = request.data.get('first_name', '')
          if first_name:
               all_users = User.objects.filter(first_name__icontains=first_name)
          else:
               return Response({"error":"Please provide a first name"}, status=status.HTTP_400_BAD_REQUEST)
          serializer = UserSerializer(all_users, many=True)
          return Response({
                          "serializer": serializer.data,
                           },
                          status=status.HTTP_200_OK)


# Friend Request View Set
class FriendRequestViewSet(viewsets.ViewSet):

     @action(detail=True, methods=['Post'])
     def friend_request(self,request,pk=None, friend_pk=None):
          user = User.objects.get(pk=pk)
          new_friend = get_object_or_404(User, pk=friend_pk)


          if new_friend in user.friend.all():
               return Response({'Detail':'Already friends'}, status=status.HTTP_400_BAD_REQUEST)
          
          user.friend.add(new_friend)

          return Response({"Detail":f"Successfully {new_friend} added"}, status=status.HTTP_200_OK)
          

# All Friend View Set          
class AllFriendsViewSet(viewsets.ViewSet):
     
     @action(detail=True, methods=['Get'])
     def all_friends(self,request, pk=None):
          user = User.objects.get(pk=pk)
          friends = user.friend.all()
          number_of_friends = user.friend.count()

          user_serializer = UserSerializer(user)
          friends_serializer = UserSerializer(friends, many=True)

          return Response({"user":user_serializer.data,
                           "number_of_friend":number_of_friends,
                           "friends":friends_serializer.data
                           }, status=status.HTTP_200_OK)
     

# DeleteFriend
class DeleteFriend(viewsets.ViewSet):

     @action(detail=True, method=['Delete'])
     def delete_friend(self,request,pk=None, friend_pk=None):

          user = User.objects.get(pk=pk)
          friend = User.objects.get(pk=friend_pk)

          if friend in user.friend.all():
               user.friend.remove(friend)
               return Response({"message":f"you friend {friend} is no more your friend which is sad"})
     

# ComementViewSet
class CommentViewSet(viewsets.ViewSet):

     @action(detail=True, method=['Post'])
     def comments(self, request, pk=None, post_pk=None, friend_pk=None):
          user= User.objects.get(pk=pk)
          post = Post.objects.get(pk=post_pk)
          friend_comment = User.objects.get(pk=friend_pk)

          if request.method == 'POST':
               user_serializer = UserSerializer(user)
               post_serializer = PostSerializer(post)

               friend_comment_serializer = CommentSerializer(data=request.data)
               if friend_comment_serializer.is_valid():
                    friend_comment_serializer.save(user=friend_comment, post=post)

                    return Response({"user":user_serializer.data,
                                "post_serializer":post_serializer.data,
                                "friend_comment": friend_comment_serializer.data
                                }, status=status.HTTP_200_OK)
               
               
# UpdateCommentViewSet 
class UpdateCommentViewSet(viewsets.ViewSet):

     @action(detail=True, method=['Put','Delete'])
     def update_comment(self,request, pk=None,post_pk=None, friend_pk=None, comment_pk=None):

          user = User.objects.get(pk=pk)
          post = Post.objects.get(pk=post_pk)
          friend = User.objects.get(pk=friend_pk)
          comment = Comment.objects.get(pk=comment_pk)


          if request.method == 'PUT':
               user_serializer = UserSerializer(user)
               friend_serializer = UserSerializer(friend)
               post_serializer = PostSerializer(post)
               updated_comment_serializer = CommentSerializer(comment, data=request.data)
               
               
               if updated_comment_serializer.is_valid():
                    updated_comment_serializer.save(user=friend, post=post)

                    return Response({"updated_friend_comment": updated_comment_serializer.data
                                }, status=status.HTTP_200_OK)
               
          if request.method == 'DELETE':
               comment.delete()
               return Response({
                    "message":f"you comment {comment.text} has beed deleted successfully"},
                    status= status.HTTP_200_OK)
                               

# LikeViewSet
class LikeViewSet(viewsets.ViewSet):

     @action(detail=True, method='Post')
     def likes(self,request,pk=None, post_pk=None):

          user = User.objects.get(pk=pk)
          post = Post.objects.get(pk=post_pk)
          like = request.data.get('likes')


          if like:
               if post.likes.filter(id=user.id).exists():
                    return Response({"message":"User already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
               
               else:
                    post.likes.add(user)
                    post.save()
                    post_serializer=PostSerializer(post)
                    return Response({'message':f'{user.first_name} liked',
                                     'post':post_serializer.data,
                                     'likes_count': post.likes.count()}, 
                                     status=status.HTTP_200_OK)
          
          else:
               if post.likes.filter(id=user.id).exists():
                    post.likes.remove(user)
                    post_serializer=PostSerializer(post)
                    return Response({'message':f'{user.first_name} unliked the post',
                                     'post':post_serializer.data,
                                     'likes_count': post.likes.count()}, 
                                      status=status.HTTP_200_OK)
               
          return Response({'post':post,
                           'likes_count': post.likes.count()},
                          status=status.HTTP_200_OK)
          


class SettingViewSet(viewsets.ViewSet):

     @action(detail=True, method='Put')
     def update_name(self,request,pk=None):

          user = User.objects.get(pk=pk)
          serializer = UserSerializer(user, data=request.data, partial=True)
          if serializer.is_valid():
               serializer.save()
               return Response({"message":"updated"},
                          status=status.HTTP_200_OK)

 
     



         




         
          




      






