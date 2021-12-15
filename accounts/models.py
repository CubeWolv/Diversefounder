from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



class Profile(models.Model):
    user1= models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profileimg = models.ImageField(
        upload_to='pics/', default='default.png', null=True, blank=True)
    bio = models.TextField()
    country = models.CharField(max_length=30)
    website = models.CharField(max_length=200)
    istagram = models.CharField(max_length=200)
    facebook = models.CharField(max_length=200)
    linkedin = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200) 

    def __str__(self):
        return '%s %s' % (self.user1.first_name, self.user1.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user1=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
