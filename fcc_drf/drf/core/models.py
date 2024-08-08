from django.db import models
import uuid
# Create your models here.

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, verbose_name="Name")
    message = models.TextField(blank=True, null=True, verbose_name="Message")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    modified = models.DateTimeField(auto_now=True, verbose_name="Modified")
    status = models.BooleanField(default=True, verbose_name="Status")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.name