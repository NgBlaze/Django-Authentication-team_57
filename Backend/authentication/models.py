from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from email.policy import default
from operator import mod
from turtle import title
from django.db import models
# Create your models here.

# Extending User Model Using a One-To-One Lin
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

def save(self, *args, **kwargs):
    super(Profile).save()

    img = Image.open(self.avatar.path)

    if img.height > 100 or img.width > 100:
        new_img = (100, 100)
        img.thumbnail(new_img)
        img.save(self.avatar.path)
        

class Contact(models.Model):
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	email_address = models.EmailField(max_length = 150)
	message = models.TextField(blank=True, null=True)