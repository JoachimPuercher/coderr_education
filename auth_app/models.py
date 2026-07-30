from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserTypeChoices(models.TextChoices):
    CUSTOMER = "customer"
    BUSINESS_USER = "business_user"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(choices=UserTypeChoices.choices, max_length=20)