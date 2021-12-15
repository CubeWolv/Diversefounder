from django.db import models

# Create your models here.
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField 
from django.utils import timezone
from accounts.models import Profile

# Create your models here.


class Campaign(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True)
    fullname = models.CharField(max_length=255, blank=True)
    websiteURL = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True) 
    zipcode = models.CharField(max_length=255, blank=True)
    campaignName = models.CharField(max_length=255, blank=True)
    campaignTagline = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    startdate = models.DateTimeField(default=timezone.now  ,blank=True, null=True)
    enddate = models.DateTimeField(default=timezone.now  ,blank=True, null=True)
    pitchFile =models.ImageField(
        upload_to='files/', default='campaign.png', null=True, blank=True)
    vidlink = models.CharField(max_length=255, blank=True)
    campaignPitch =  HTMLField()
    campaignGoal = models.CharField(max_length=255, blank=True)
    faqs = models.TextField(blank=True)
    currentdate= models.DateField(default=timezone.now)
    liked = models.ManyToManyField(User ,default=None, blank=True, related_name="liked")
    is_complete = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s' % (self.fullname ,self.campaignName)

class update(models.Model):
    campaign=models.ForeignKey(Campaign,  related_name='updates' ,on_delete=models.CASCADE)
    updatetitle=models.CharField(max_length=255 ,blank=True)
    body= models.TextField()

    def __str__(self):
        return '%s - %s' % (self.campaign ,self.title)

class reward(models.Model):
    campaign = models.ForeignKey(Campaign,  related_name='rewards' ,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    title = models.CharField(max_length=255, blank=True)
    rewarddetails= HTMLField()
    rewardpicture =models.ImageField(
        upload_to='files/', default='campaign.png', null=True, blank=True) 
    shippinginfo = models.TextField(blank=True)
    total_available = models.IntegerField(default=0)
    year= models.CharField(max_length=255, blank=True)
    month=models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title





class Comment(models.Model):
    campaign=models.ForeignKey(Campaign,  related_name='comments' ,on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    currentdate = models.DateTimeField()

    def __str__(self):
        return '%s -%s'% (self.name ,self.currentdate)

