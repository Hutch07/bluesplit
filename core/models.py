from django.contrib.auth.models import AbstractUser
from django.db import models


class Group(models.Model):
    ADMIN = 'Admin'
    PILOT = 'Pilot'
    CUSTOMER = 'Customer'
    GENERAL = 'General'

    GROUP_CHOICES = [
        (ADMIN, 'Admin'),
        (PILOT, 'Pilot'),
        (CUSTOMER, 'Customer'),
        (GENERAL, 'General'),
    ]

    name = models.CharField('Name', max_length=20, choices=GROUP_CHOICES, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'


class User(AbstractUser):
    company = models.CharField('Company', max_length=255, blank=True)
    group = models.ManyToManyField(Group, related_name='users', blank=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Site(models.Model):
    name = models.CharField('Name', max_length=255, unique=True)
    longitude = models.FloatField('Longitude')
    latitude = models.FloatField('Latitude')
    allowed_users = models.ManyToManyField(
        'User',
        related_name='allowed_sites',
        blank=True,
        verbose_name='Allowed Users',
    )
    default_style = models.CharField('Default Style', max_length=16, unique=False, default='split')

    def __str__(self):
        return self.name + ', ' + str(self.default_style)

    class Meta:
        verbose_name = 'site'
        verbose_name_plural = 'sites'


class Flight(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='flights')
    aws_url = models.CharField('AWS URL', max_length=500, unique=True)
    date = models.DateField('Date')
    pilot = models.CharField('Pilot', max_length=32)

    def __str__(self):
        return f"Flight on {self.date} by {self.pilot}"

    class Meta:
        verbose_name = 'flight'
        verbose_name_plural = 'flights'


class Geojson(models.Model):
    name = models.CharField('Name', max_length=255, unique=True)
    url = models.TextField('URL', unique=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='geojsons')
    level = models.IntegerField('Level', default=1, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'geojson'
        verbose_name_plural = 'geojsons'


class Obscure(models.Model):
    """
    Cloud Optimized GeoTIFF (COG) layer for terrain masking or obscuring.
    Admins only. These layers are always displayed and cannot be toggled off.
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='obscures')
    aws_url = models.CharField('AWS COG URL', max_length=500, unique=True)
    name = models.CharField('Name', max_length=255, blank=True, help_text='Optional display name for the COG layer')
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    def __str__(self):
        return f"{self.site.name} - {self.name or 'Obscure Layer'}"

    class Meta:
        verbose_name = 'obscure'
        verbose_name_plural = 'obscures'
