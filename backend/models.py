from django.db import models


# Create your models here.

class User(models.Models):
    user_id = models.AutoField(primary=True)
    first_name = models.CharField(max_legnth=50)
    last_name = models.CharField(max_legnth=50)
    email = models.EmailField(max_legnth=100, unique=True)
    password = models.CharField(max_legnth=20)
    profile_image = models.URLField(max_legnth=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)







