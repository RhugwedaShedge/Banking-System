from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    account_no = models.IntegerField()
    cif_no = models.IntegerField()
    mobile_no = PhoneNumberField()

    def __str__(self):
        return str(self.user)


    

