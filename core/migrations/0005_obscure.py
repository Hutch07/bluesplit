from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_geojson_level_site_allowed_users_site_default_style'),  # ← FIXED: Changed from 0004 to 0003
    ]

    operations = [
        migrations.CreateModel(
            name='Obscure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aws_url', models.CharField(max_length=500, unique=True, verbose_name='AWS COG URL')),
                ('name', models.CharField(blank=True, help_text='Optional display name for the COG layer', max_length=255, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='obscures', to='core.site')),
            ],
            options={
                'verbose_name': 'obscure',
                'verbose_name_plural': 'obscures',
            },
        ),
    ]
