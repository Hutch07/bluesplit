from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Group, User, Site, Flight, Geojson, Obscure


class UserAdmin(BaseUserAdmin):
    """Custom user admin that includes company and group fields."""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('company', 'group')}),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude')  # Removed default_style
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('site', 'date', 'pilot')
    list_filter = ('site', 'date')
    search_fields = ('site__name', 'pilot')
    ordering = ('-date',)


@admin.register(Geojson)
class GeojsonAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'level')
    list_filter = ('site', 'level')
    search_fields = ('name', 'site__name')
    ordering = ('site', 'level', 'name')


@admin.register(Obscure)
class ObscureAdmin(admin.ModelAdmin):
    """
    Admin interface for Cloud Optimized GeoTIFF layers.
    Restricted to superusers/admins only.
    """
    list_display = ('site', 'name', 'created_at', 'updated_at')
    list_filter = ('site', 'created_at')
    search_fields = ('name', 'site__name', 'aws_url')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Site & Layer Info', {
            'fields': ('site', 'name')
        }),
        ('AWS COG URL', {
            'fields': ('aws_url',),
            'description': 'Cloud Optimized GeoTIFF URL from AWS S3'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Only superusers can add Obscure layers."""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete Obscure layers."""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Only superusers can change Obscure layers."""
        return request.user.is_superuser


# Register other models
admin.site.register(User, UserAdmin)
