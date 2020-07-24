from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=20)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

