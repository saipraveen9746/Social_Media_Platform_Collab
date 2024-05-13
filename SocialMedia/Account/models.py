from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.forms import ValidationError
import phonenumbers


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=email, username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    follower = models.ManyToManyField('self',related_name='following_profiles',blank=True,symmetrical=False)
    following = models.ManyToManyField('self',related_name='follower_profiles',blank=True,symmetrical=False)
    name = models.CharField(max_length=200,null=True)
    dob = models.DateField(null=True)
    phone_number = models.CharField(max_length=20,null=True)
    location = models.CharField(max_length=200,null=True)





    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    def follower_count(self):   
        return self.follower.count()
    def follower_usernames(self):
        return [user.username  for user in self.follower.all()]
    def following_count(self):
        return self.following.count()
    def following_names(self):
        return [user.username for user in self.following.all()]
    def clean(self):
        super().clean()
        try:
            parsed_number = phonenumbers.parse(self.phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number format")


    @property
    def is_staff(self):
        return self.is_admin
        
    def fill_bio(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()



