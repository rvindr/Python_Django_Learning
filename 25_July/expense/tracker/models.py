from django.db import models
import uuid
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """
    Abstract base model with common fields for other models.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True, max_length=100)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Transaction(BaseModel):
    """
    Model representing a financial transaction.
    """
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def is_negative(self):
        """
        Check if the transaction amount is negative.
        """
        return self.amount < 0
