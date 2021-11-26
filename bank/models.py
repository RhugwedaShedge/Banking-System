from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from phone_field import PhoneField


class Customer(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    # account_no = models.IntegerField(max_digits=20)
    # cif_no = models.IntegerField(max_digits=20)
    # PhoneField(blank=True, help_text='Contact phone number')

    

