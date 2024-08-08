from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=1000)
    desc = models.TextField()
    img = models.URLField()
    external_link = models.URLField()