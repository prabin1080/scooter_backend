from django.db import models
from django.conf import settings

# Create your models here.

class HelmetSlot(models.Model):
    is_empty = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)


class BookingCount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='helmet_bookings')
    count = models.IntegerField(default=0)
    is_scooter_rented = models.BooleanField(default=False)