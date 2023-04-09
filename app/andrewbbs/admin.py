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
    list_display = ('handle','joined_on', 'phone', 'first_name', 'last_name', 'zip', 'get_groups', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('handle', 'phone', 'first_name', 'last_name', 'zip')
    readonly_fields = ('unlocked_codes',)
    list_filter = ('groups',)

    # joined on is created at time at YYYY-MM-DD HH:MM:SS
    joined_on = lambda self, obj: obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    joined_on.short_description = 'Joined On'

    # get groups is a comma separated list of groups
    get_groups = lambda self, obj: ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Groups'

admin.site.register(Screen, ScreenAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(Member, MemberAdmin)