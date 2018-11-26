from django.db import models
from django.contrib.auth.models import User
# from annoying.fields import AutoOneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Town(models.Model):
    name = models.CharField(max_length=20, unique=True)
    bio = models.CharField(max_length=40, default='')
    admin = models.ForeignKey(User, related_name='administrate')

    def save_town(self):
        self.save()

    def remove_town(self):
        self.delete()

    @classmethod
    def get_town(cls, id):
        town = Town.objects.get(id=id)
        return town


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=25, unique=True)
    bio = models.TextField(max_length=100, blank=True)
    profilepic = models.ImageField(upload_to='picture/', default=True)
    email = models.EmailField()
    contact = models.CharField(max_length=15, blank=True)
    townpin = models.BooleanField(default=False)
    town = models.ForeignKey(Town, related_name='home', null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    @classmethod
    def search_by_username(cls, search_query):
        profiles = cls.objects.filter(user__username__icontains=search_query)
        return profiles

    @classmethod
    def updateimage(cls, id):
        image = cls.objects.get(id=id)
        return image


class Post(models.Model):
    title = models.CharField(max_length=30)
    post = models.TextField(max_length=100)
    hood = models.ForeignKey(Town, related_name='town')
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    postpic = models.ImageField(upload_to='picture/', default=True)

    def save_post(self):
        self.save()

    def remove_post(self):
        self.delete()

    @classmethod
    def get_town_posts(cls, id):
        posts = Post.objects.filter(id=id)
        return posts

    @classmethod
    def post_comments(cls, id):
        comments = cls.objects.filter(postcomments__comment_id=id)
        posters = cls.objects.filter(postcomments__commnetator__id=id)
        return comments, posters


class Comment(models.Model):
    comment = models.CharField(max_length=100)
    commentator = models.ForeignKey(User)
    comment_post = models.ForeignKey(Post, related_name='comment', null=True)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()
