from django.urls import path, include
from . import views
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView




router = routers.DefaultRouter()
router.register('signup', views.SignupViewSet, basename='signup')
router.register('login', views.LoginViewSet, basename='login')

login_router = routers.NestedDefaultRouter(router, 'login', lookup='login')
login_router.register('home', views.HomeViewSet, basename='home')

login_router.register('home/createpost', views.CreatePostViewSet, 'createpost')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(login_router.urls)),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


