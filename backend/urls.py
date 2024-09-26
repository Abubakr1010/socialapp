from django.urls import path, include
from . import views
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView



urlpatterns = [
    path('signup/', views.SignupViewSet.as_view({'post': 'signup'}, name='signup')),
    path('login/', views.LoginViewSet.as_view({'post': 'login'}), name='login'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


