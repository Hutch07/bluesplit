from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_geojson_level_site_allowed_users_site_default_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='default_style',
        ),
    ]
