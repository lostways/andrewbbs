from django.contrib import admin

# Register your models here.
from .models import Screen
from .models import AccessCode


class ScreenAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published')
    search_fields = ('title', 'body')

class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid')
    search_fields = ('title', 'body')

admin.site.register(Screen, ScreenAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)
