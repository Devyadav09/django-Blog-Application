from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField

from .helpers import *




class BlogModel(models.Model):
    userid=models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    content = FroalaField(options={
        'imageUploadURL': '/media/',  # URL to your image upload endpoint
        })
    slug = models.SlugField(max_length=1000)
    image = models.ImageField(upload_to='blog', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)   
   
    upload_at = models.DateTimeField(auto_now=True)        
    
    
    
    # show date when blog is update when any field of blog is update its show
      #created at once when blog is created show created date
     
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel,self).save(*args,**kwargs)
        
        
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)   
    upload_at = models.DateTimeField(auto_now=True)        
     

    def __str__(self):
        return self.user.username +  " Comment: " + self.content
    
    