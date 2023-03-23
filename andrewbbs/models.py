from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class AccessCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code

    def has_screens(self):
        return Screen.objects.filter(codes__in=[self]).exists()

class Screen(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='screens')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    codes = models.ManyToManyField(AccessCode, blank=True,
                                   related_name="screens")  

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class MemberManager(BaseUserManager):
    def create_user(self, handle, phone, password, **other_fields):
        if not handle:
            raise ValueError('Users must have a handle')
        
        if not phone:
            raise ValueError('Users must have a phone')

        if password is not None:
            user = self.model(
                handle=handle,
                phone=phone,
                password=password,
                **other_fields,
            )
            user.save()
        else:
            if other_fields.get('is_staff') is True:
                raise ValueError('Staff must have a password')
            user = self.model(
                handle=handle,
                phone=phone,
                password=password,
                **other_fields,
            )
            user.set_unusable_password()
            user.save() 

        return user

    def create_superuser(self, handle, phone, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(handle, phone, password, **other_fields)
        user.set_password(password)
        user.save()

        return user

class Member(AbstractBaseUser, PermissionsMixin):
    handle = models.CharField(max_length=100, unique=True)
    phone = PhoneNumberField(blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    unlocked_codes = models.JSONField(blank=True, null=False, default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'handle'
    REQUIRED_FIELDS = ['phone']

    objects = MemberManager()

    class Meta:
        ordering = ['handle']

    def __str__(self):
        return self.handle
