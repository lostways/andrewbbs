from django.contrib import admin

# Register your models here.
from .models import Screen
from .models import AccessCode
from .models import Member


class ScreenAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published')
    search_fields = ('title', 'body')

class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'enabled')
    search_fields = ('title', 'body')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('handle', 'phone', 'first_name', 'last_name', 'zip')
    search_fields = ('handle', 'phone', 'first_name', 'last_name', 'zip')
    readonly_fields = ('unlocked_codes',)

admin.site.register(Screen, ScreenAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(Member, MemberAdmin)