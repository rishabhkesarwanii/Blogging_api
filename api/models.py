from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blogs(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    #this is to make sure that when a user is deleted, all their blogs are deleted as well
    #User ForeignKey is used to create a one-to-many relationship with the User model
    title = models.CharField(max_length=100) #CharField for the title
    content = models.TextField()    #TextField for the content
    image = models.ImageField(upload_to='images/', null=True, blank=True) #ImageField for the image(Pillow)
    date_created = models.DateTimeField(auto_now_add=True) #DateTimeField for the date created

    def __str__(self):
        return self.title   #return the title of the blog
    
