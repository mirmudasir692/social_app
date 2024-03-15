from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from utils.accounts import AccountsServicesClass
from django.contrib.auth import authenticate
from datetime import datetime

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
            # result = AccountsServicesClass.verify_mobile_number(number)
            result = True
            if result:
                return number
            else:
                raise ValueError("Invalid Mobile number")
        else:
            raise  ValueError("Mobile number cannot be empty")

    @classmethod
    def validate_username(cls, username):
        """
        check for user, does username is associated with any user
        :param username:
        :return:
        """
        if not User.objects.filter(username=username).exists():
            return username
        else:
            raise ValueError("User with this username already exists")

    @classmethod
    def validate_email(cls, email):
        """
        validate email with external service
        :param email:
        :return:
        """
        if not User.objects.filter(email=email).exists():
            # is_email_valid = AccountsServicesClass.verify_email(email)
            is_email_valid = True
            if is_email_valid:
                return email
            else:
                raise ValueError("Email is not valid")
        else:
            raise ValueError("this email is already associated with account")


    @classmethod
    def validate_dob(cls, dob):
        print(dob)
        print(type(dob))

        current_year = datetime.now().year
        birth_year = dob.year
        age = current_year - birth_year
        # Check if the age is greater than 16
        if age >= 16:
            return dob
        else:
            raise ValueError("You must be at least 16 years old.")
        
    @classmethod
    def validate_password(cls, password):
        if len(password) > 8:
            return True
        raise ValueError("password must be at least of digits")


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, password, email, **extra_fields):
        if not username:
            raise ValueError("username is required")
        email = self.normalize_email(email)
        is_username_unique = ValidationClass.validate_username(username)
        dob = extra_fields.get("dob")
        dob_valid = ValidationClass.validate_dob(dob)
        is_password_valid = ValidationClass.validate_password(password)
        if is_username_unique and dob_valid and is_password_valid:
            if email:
                is_email_valid = ValidationClass.validate_email(email)
            if is_email_valid or email is None:
                user = self.model(username=username, email=email, **extra_fields)
                user.set_password(password)
                user.save()
                return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def authenticate_user(self, username=None, password=None):
        if username is not None and password is not None:
            user = authenticate(username=username, password=password)
            return user
        else:
            raise ValueError("please provide username and password")


class User(AbstractUser):
    username = models.CharField(max_length=155, null=False, verbose_name="username", unique=True)
    mobile = PhoneNumberField(blank=True, region="IN",null=True, verbose_name="mobile number",  unique=True)
    dob = models.DateField(null=True, verbose_name="date of birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="gender")
    verified = models.BooleanField(default=False)
    professional = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=True)
    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['mobile'], name='mobile_idx'),
        ]

    def __str__(self):
        return self.username