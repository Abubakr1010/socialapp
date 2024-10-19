from django.urls import path, include
from . import views
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView



urlpatterns = [
    path('signup/', views.SignupViewSet.as_view({'post': 'signup'}), name='signup'),
    path('login/', views.LoginViewSet.as_view({'post': 'login'}), name='login'),
    path('home/<int:pk>/', views.HomeViewSet.as_view({'get':'home'}), name='home'),
    path('create_post/<int:pk>/', views.CreatePostViewSet.as_view({'post':'create_post'}), name='create_post'),
    path('single_post/<int:pk>/<int:post_id>/', 
         views.SinglePostViewSet.as_view({'get':'single_post',
                                         'delete':'single_post',
                                         'put':'single_post'}), 
                                         name='create_post'),
    path('profile/<int:pk>/', views.Profile.as_view({'get':'profile'}), name='profile'),
    path('search/<int:pk>/', views.SearchViewSet.as_view({'post':'search'}), name='search'),
    path('friend_request/<int:pk>/<int:friend_pk>/', views.FriendRequestViewSet.as_view({'post':'friend_request'}), name='friend_request'),
    path('all_friends/<int:pk>/', views.AllFriendsViewSet.as_view({'get':'all_friends'}), name='all_friends'),
    path('delete_friend/<int:pk>/<int:friend_pk>/', views.DeleteFriend.as_view({'delete':'delete_friend'}), name='delete_friend'),
    path('comments/<int:pk>/<int:post_pk>/<int:friend_pk>/', views.CommentViewSet.as_view({'post':'comments'}), name='comments'),
    path('update_comment/<int:pk>/<int:post_pk>/<int:friend_pk>/<int:comment_pk>/', views.UpdateCommentViewSet.as_view({'put':'update_comment',
                                                                                                                        'delete':'update_comment'}), 
                                                                                                                        name='update_comment'),
    path('likes/<int:pk>/<int:post_pk>/',views.LikeViewSet.as_view({'post':'likes'}), name='likes'),
    path('update_name/<int:pk>/', views.SettingViewSet.as_view({'put':'update_name'}), name='update_name'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


