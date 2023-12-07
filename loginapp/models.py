from django.db import models


# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False, unique=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class FormData(models.Model):
    user = models.CharField(default='',max_length=100,null=False,blank=False)
    Age = models.IntegerField(default='',null=False, blank=False)
    Gender = models.CharField(max_length=10,default='none',null=False,blank=False)
    MobileNo = models.IntegerField(default='',null=False, blank=False)
    MailId = models.EmailField(default='',null=False,blank=False)
    Problems = models.CharField(max_length=50,default='none',blank=False,null=False)
    Symptoms = models.CharField(max_length=50,default='none',blank=False,null=False)
    Recommendation = models.CharField(max_length=50,default='',blank=True,null=True)
    objects = models.Manager()

    def __str__(self):
        return self.user


class Recommendation(models.Model):
    user=models.CharField(default='',max_length=100,null=False,blank=False)
    music_id=models.IntegerField(blank=True,null=True)
    raag=models.CharField(blank=False,null=False,max_length=100)
    type=models.CharField(blank=False,null=False,max_length=100)
    music=models.CharField(blank=False,null=False,max_length=100)
    music_path=models.CharField(blank=False,null=False,max_length=100,default='')
    createdAt=models.DateTimeField(blank=False,null=False,default=datetime.datetime.now())
    objects=models.Manager()

    def __str__(self):
        return self.user
    


    
