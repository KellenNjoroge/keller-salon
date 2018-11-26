from django.db import models
from django.contrib.auth.models import User
# from annoying.fields import AutoOneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # name = models.CharField(max_length=25)
    username = models.CharField(max_length=25, unique=True)
    # relate = models.ManyToManyField('self', symmetrical=False, through='Relationship')
    bio = models.TextField(max_length=100, blank=True)
    profilepic = models.ImageField(upload_to='picture/', default=True)
    email = models.EmailField()
    contact = models.CharField(max_length=15, blank=True)

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
