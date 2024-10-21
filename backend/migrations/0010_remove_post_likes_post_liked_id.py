# Generated by Django 5.1.1 on 2024-10-12 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_remove_post_likes_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='liked_id',
            field=models.ManyToManyField(blank=True, related_name='liked_post', to='backend.user'),
        ),
    ]