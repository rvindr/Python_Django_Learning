# learning soft delete and manager in django
from django.db import models


class skillManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)




class Skill(models.Model):
    skill_name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    objects = skillManager()
    new_manager = models.Manager()



    def __str__(self): return self.skill_name


