from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from utils.accounts import AccountsServicesClass
from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework.exceptions import ValidationError

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
            raise ValueError("Mobile number cannot be empty")

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
        if len(password) > 3:
            return True
        raise ValueError("password must be at least of digits")


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, password, email, **extra_fields):
        """
            Create a new user.

            :param username: The username for the new user.
            :param password: The password for the new user.
            :param email: The email address for the new user (optional).
            :param superuser: Boolean indicating whether the user should be a superuser (default: False).
            :param extra_fields: Additional fields to include when creating the user.
            :return: The newly created user object if successful, None otherwise.
            :raises ValueError: If username is not provided or if validation fails.
            """
        if not username:
            raise ValueError("username is required")
        email = self.normalize_email(email) if email else None
        is_username_unique = ValidationClass.validate_username(username)
        dob = extra_fields.get("dob", None)
        dob_valid = ValidationClass.validate_dob(dob) if dob else True
        is_password_valid = ValidationClass.validate_password(password)
        if is_username_unique and dob_valid and is_password_valid:
            is_email_valid = ValidationClass.validate_email(email) if email else True
            if is_email_valid:
                user = self.model(username=username, email=email, **extra_fields)
                user.set_password(password)
                user.save()
                return user

        return None

    def create_superuser(self,username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, email, **extra_fields)

    def authenticate_user(self, username=None, password=None):
        print("username", username)
        print("password", password)
        if username is not None and password is not None:
            user = authenticate(username=username, password=password)
            print(user)
            if not user:
                raise ValueError("Incorrect username or password")
            return user
        else:
            raise ValueError("please provide username and password")

    def deactivate_account(self, password, user):
        pass

    def delete_account(self, password, user):
        try:
            if not password:
                raise ValueError("password is required")
            if not user:
                raise ValueError("user instance is required to delete the user")
            user_instance_fetched = self.get(id=user.id)
            user_instance_logged_in = authenticate(username=user.username, password=password)
            if not user_instance_logged_in:
                raise ValueError("Invalid password")
            if user_instance_fetched == user_instance_logged_in:
                user_instance_logged_in.delete()
                return {"message": "User account deleted successfully"}
        except Exception as e:
            return {"error": str(e)}

    def get_friend_profile(self, user_id):
        user_profile = User.objects.prefetch_related("moments", "blogs").get(id=user_id)

        return {'user_profile': user_profile, 'moments': user_profile.moments.all(), 'blogs': user_profile.blogs.all()}

    @staticmethod
    def default_profile_pic():
        return "/user placeholder/avatar-1577909_1280.png"


class User(AbstractUser):
    username = models.CharField(max_length=155, null=False, verbose_name="username", unique=True)
    name = models.CharField(max_length=255, null=True, verbose_name="name")
    mobile = PhoneNumberField(blank=True, region="IN", null=True, verbose_name="mobile number",  unique=True)
    dob = models.DateField(null=True, verbose_name="date of birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="gender")
    verified = models.BooleanField(default=False)
    professional = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=True)
    profile_pic = models.ImageField(upload_to="user_profiles", null=True, default=UserManager.default_profile_pic)
    bio = models.TextField(default="", blank=True)
    num_blogs = models.IntegerField(default=0)
    num_moments = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    USERNAME_FIELD = "username"
    followers_num = models.BigIntegerField(default=0)
    following_num = models.BigIntegerField(default=0)

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['mobile'], name='mobile_idx'),
        ]

    def __str__(self):
        return self.username


class FollowManager(models.Manager):
    def follow_user(self, follower_id, followed_user_id):
        if not follower_id or not followed_user_id:
            raise ValidationError("both fields are required")
        try:
            follow_item, created = self.get_or_create(follower_id=follower_id, followed_user_id=followed_user_id)
            if not created:
                follow_item.delete()
            return True
        except self.model.DoesNotExist:
            raise ValueError("something went wrong")

    def get_all_followers(self, user_id):
        followers = self.filter(followed_user_id=user_id).values_list('follower', flat=True)
        return User.objects.filter(id__in=followers)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FollowManager()

    def __str__(self):
        return f"{self.follower} follows {self.followed_user}"



