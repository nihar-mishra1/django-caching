from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        This Function creates a user with given credentials
        """
        if not email:
            raise ValueError("User Must Have an Email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        This function will create a super user
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    It Creates Custom User Model Inherited from Abstarctbaseuser
    """
    email = models.EmailField(max_length=255, unique=True, validators=[validators.validate_email])
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=222, blank=True)
    state = models.CharField(max_length=33)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'address', 'state']


class Property(models.Model):

    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'

    class HomeType(models.TextChoices):
        HOUSE = 'House'
        VILLA = 'Villa'

    seller = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='properties')
    title = models.CharField(max_length= 111)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=54)
    state = models.CharField(max_length= 20)
    sale_type = models.CharField(max_length=30, choices = SaleType.choices, default = SaleType.FOR_SALE)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathroom = models.IntegerField()
    home_type = models.CharField(max_length=50, choices=HomeType.choices, default=HomeType.HOUSE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return self.title


# Method for updating cache after model update
@receiver(post_save, sender=Property)
def clear_cache(sender, instance, **kwargs):
    cache.clear()
