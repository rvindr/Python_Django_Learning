from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from PIL import Image
import os
# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=(('male','male'),('female','female')))
    student_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.student_name
    

@receiver(pre_delete, sender=Student )
def save_student(sender, instance, **kwargs):
    print(f'{instance.student_name} with student id {instance.student_id} is deleted.')

@receiver(post_save, sender=Student )
def save_student(sender, instance,created, **kwargs):
    if created:
        instance.student_id = f'STU-000{instance.id}'
        instance.save()
        print("Student object created")


class Images(models.Model):

    original_img = models.ImageField(upload_to='image')
    thumb_small = models.ImageField(upload_to='image/thumbnails', blank=True, null=True)
    thumb_medium = models.ImageField(upload_to='image/thumbnails', blank=True, null=True)
    thumb_large = models.ImageField(upload_to='image/thumbnails', blank=True, null=True)

@receiver(post_save,sender = Images)
def create_thumbnail(sender, instance, created, **kwargs):
    if created:
        sizes = {
            'thumb_small' : (100,100),
            'thumb_medium' : (300,300),
            'thumb_large' : (600,600)
        }

        for fields, size in sizes.items():
            img = Image.open(instance.original_img.path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            thumb_name, thumb_extension = os.path.split(instance.original_img.name)
            thumb_filename = f'{thumb_name}_{size[0]}*{size[1]}{thumb_extension}'
            thumb_path = f'thumbnails/{thumb_filename}'
            img.save(thumb_path)

            setattr(instance, fields, thumb_path)

        instance.save(update_fields=sizes.keys())