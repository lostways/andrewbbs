import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
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

    def has_unread_messages(self):
        return Message.objects.unread_messages_count(self) > 0

    class Meta:
        ordering = ['handle']

    def __str__(self):
        return self.handle

class MessageManager(models.Manager):
    def sent_messages(self, user):
        return super().get_queryset().filter(sender=user)

    def received_messages(self, user):
        return super().get_queryset().filter(recipient=user)

    def unread_messages(self, user):
        return super().get_queryset().filter(recipient=user, read=False)

    def read_messages(self, user):
        return super().get_queryset().filter(recipient=user, read=True)
    
    def unread_messages_count(self, user):
        return super().get_queryset().filter(recipient=user, read=False).count()
         


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=300, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    objects = MessageManager()

    def mark_read(self):
        self.read = True
        self.save()
    
    def get_absolute_url(self):
        return reverse('member-message-detail', args=[str(self.uuid)])

    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Messsage from {self.sender} to {self.recipient}"
