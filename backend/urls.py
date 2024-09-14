from django.urls import path, include
from . import views
from rest_framework_nested import routers




router = routers.DefaultRouter()
router.register('signup', views.SignupViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
]