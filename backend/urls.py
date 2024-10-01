from django.urls import path, include
from . import views
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView



urlpatterns = [
    path('signup/', views.SignupViewSet.as_view({'post': 'signup'}, name='signup')),
    path('login/', views.LoginViewSet.as_view({'post': 'login'}), name='login'),
    path('home/<int:pk>/', views.HomeViewSet.as_view({'get':'home'}), name='home'),
    path('create_post/<int:pk>/', views.CreatePostViewSet.as_view({'post':'create_post'}), name='create_post'),
    path('single_post/<int:pk>/post/<int:post_id>/', 
         views.SinglePostViewSet.as_view({'get':'single_post',
                                         'delete':'single_post'}), 
                                         name='create_post'),
    path('all_posts/<int:pk>/', views.UserAllPosts.as_view({'get':'all_posts'}), name='all_posts'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


