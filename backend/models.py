from django.db import models


# Create your models here.

class User(models.Models):
    user_id = models.AutoField(primary=True, auto_now_add=True)
    first_name = models.CharField(max_legnth=50)
    last_name = models.CharField(max_legnth=50)
    email = models.EmailField(max_legnth=100, unique=True)
    password = models.CharField(max_legnth=20)
    profile_image = models.URLField(max_legnth=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

class Post(models.MOdels):
    post_id = models.CharField(primary=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    post_text = models.CharField(max_legnth=500)
    post_image = models.URLField(max_legnth=250)
    likes = models.IntegerField()


class Comments(models.Model):
    comment_id = models.IntegerField(primary=True)
    post_id = models.ForeignKey(Post)
    user_id = models.ForeignKey(User)
    text = models.CharField(max_legnth=500)






