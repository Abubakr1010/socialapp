from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group, Permission


# User Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
   
class User(AbstractBaseUser, PermissionsMixin):
        id = models.AutoField(primary_key=True)
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        email = models.EmailField(max_length=100, unique=True)
        profile_image = models.URLField(max_length=500, blank=True, null=True)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        friend = models.ManyToManyField('self',symmetrical=False,blank=True)

        objects = CustomUserManager()
        USERNAME_FIELD = 'email'

         # Set related_name to avoid clashes with Django's default User model
        groups = models.ManyToManyField(
            Group,
            related_name='custom_user_set',
            blank=True,
        )
        user_permissions = models.ManyToManyField(
            Permission,
            related_name='custom_user_permissions_set',
            blank=True,
        )

# Post Model
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    post_text = models.CharField(max_length=500, blank=True, null=True)
    post_image = models.URLField(max_length=250, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_post', blank=True)


    def update_like_count(self):
        self.like_count = self.likes_count()
        self.save()

# Comment Model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)



