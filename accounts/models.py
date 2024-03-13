from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from utils.accounts import AccountsServicesClass

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)
class ValidationClass:
    @classmethod
    def validate_mobile(cls, number):
        """this method in the Validation class serves as validator for the mobile number"""
        if number:
            result = AccountsServicesClass.verify_mobile_number(number)
            if result:
                return number
            else:
                raise ValueError("Invalid Mobile number")
        else:
            raise  ValueError("Mobile number cannot be empty")

    @classmethod
    def validate_username(cls, username):
        if not User.objects.filter(username=username).exists():
            return username
        else:
            raise ValueError("User with this username already exists")

    @classmethod
    def validate_email(cls, email):
        if not User.objects.filter(email=email).exists():
            is_email_valid = AccountsServicesClass.verify_email(email)
            if is_email_valid:
                return email
            else:
                raise ValueError("Email is not valid")
        else:
            raise ValueError("this email is already associated with account")

    @classmethod
    def validate_dob(cls, dob):
        dob_parts = dob.split("-")
        if dob_parts[0] > 16:
            return dob
        else:
            raise ValueError("your age must be greater than 16")


class User(AbstractUser):
    username = models.CharField(max_length=155, null=False, verbose_name="username", validators=[ValidationClass.validate_username], unique=True)
    mobile = PhoneNumberField(blank=True, region="IN", verbose_name="mobile number", validators=[ValidationClass.validate_mobile], unique=True)
    dob = models.DateField(null=True, verbose_name="date of birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="gender")
    verified = models.BooleanField(default=False)
    professional = models.BooleanField(default=False)
    email = models.EmailField(validators=[ValidationClass.validate_email], unique=True)
    USERNAME_FIELD = "username"

    class Meta:
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['mobile'], name='mobile_idx'),
        ]

    def __str__(self):
        return self.username