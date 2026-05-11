from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Site, Flight, Geojson, Group


class AdminOnlyMixin:
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.group.filter(name='Admin').exists()

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)


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
