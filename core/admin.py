from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Site, Flight, Geojson, Group


def is_admin_user(user):
    """
    Returns True if the user should have admin panel access.
    Checks:
      1. is_superuser — always allowed
      2. core.Group (custom) named 'Admin'
      3. Django's built-in auth.Group named 'Admin'
    Note: user must also have is_staff=True to enter the admin at all.
    """
    if user.is_superuser:
        return True
    if user.group.filter(name='Admin').exists():
        return True
    if user.groups.filter(name='Admin').exists():
        return True
    return False


class AdminOnlyMixin:
    def has_module_permission(self, request):
        return is_admin_user(request.user)

    def has_view_permission(self, request, obj=None):
        return is_admin_user(request.user)

    def has_add_permission(self, request):
        return is_admin_user(request.user)

    def has_change_permission(self, request, obj=None):
        return is_admin_user(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin_user(request.user)


@admin.register(User)
class UserAdmin(AdminOnlyMixin, BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'company')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'group')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'company', 'password1', 'password2', 'is_staff', 'is_superuser', 'groups', 'group'),
        }),
    )
    list_display = ('username', 'email', 'company', 'is_staff')
    search_fields = ('username', 'email', 'company')
    ordering = ('username',)


@admin.register(Group)
class GroupAdmin(AdminOnlyMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Site)
class SiteAdmin(AdminOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude')
    search_fields = ('name',)


@admin.register(Flight)
class FlightAdmin(AdminOnlyMixin, admin.ModelAdmin):
    list_display = ('aws_url', 'date', 'pilot', 'site')
    search_fields = ('aws_url', 'pilot')
    list_filter = ('date', 'site')


@admin.register(Geojson)
class GeojsonAdmin(AdminOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'url', 'site')
    search_fields = ('name', 'url')
