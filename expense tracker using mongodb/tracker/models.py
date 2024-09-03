from django.db import models


class ExpenseModel(models.Model):
    description = models.TextField()
    amount = models.FloatField()
