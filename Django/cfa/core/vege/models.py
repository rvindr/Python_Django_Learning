from django.db import models

class Recipe(models.Model):

    recipe_name = models.CharField(max_length=100)
    recipe_desc = models.TextField()
    recipe_img = models.ImageField(upload_to='recipe')

    def __str__(self):
        return self.recipe_name