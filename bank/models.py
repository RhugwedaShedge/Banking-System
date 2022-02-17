from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField

TRANSFER_TYPE = (
    ("IMPS", "IMPS"),
    ("NEFT", "NEFT"),
    ("RTGS", "RTGS"),
)


class UserBankAccount(models.Model):
    user               = models.OneToOneField(User, related_name='account', on_delete = models.CASCADE)
    account_no         = models.PositiveIntegerField(unique=True)
    cif_no             = models.IntegerField()
    mobile_no          = models.CharField(max_length = 11)
    is_mobile_verified = models.BooleanField(default = False)
    balance            = models.DecimalField(default = 10000, max_digits = 12, decimal_places = 2)
    otp                = models.CharField(max_length = 7, null=True)

    def __str__(self):
        return str(self.user)

class Transaction(models.Model):
    userAccount   = models.ForeignKey(UserBankAccount, on_delete=models.SET_NULL, blank=True, null=True)  
    payeeAccount  = models.PositiveIntegerField()
    amount        = models.DecimalField(decimal_places = 2, max_digits = 20)
    remark        = models.CharField(max_length = 500, null = True)
    transfer_type = models.CharField(max_length = 20, choices = TRANSFER_TYPE, default = 'IMPS')
    date_created  = models.DateTimeField(auto_now_add = True, null = True)
    
    def __str__(self):
        return str(self.userAccount)

        



