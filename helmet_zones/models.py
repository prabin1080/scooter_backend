from django.db import models

# Create your models here.

class HelmetSlot(models.Model):
    is_empty = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)