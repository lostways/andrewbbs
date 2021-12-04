from django.db import models
from django.contrib.auth.models import User

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

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='screens')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    codes = models.ManyToManyField(AccessCode, blank=True,
                                   related_name="screens")  

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
