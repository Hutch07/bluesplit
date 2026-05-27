from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_merge_0004_remove_site_default_style_0005_obscure'),
    ]

    operations = [
        migrations.AddField(
            model_name='geojson',
            name='color',
            field=models.CharField(
                'Color',
                max_length=64,
                blank=True,
                default='cornflowerblue',
                help_text='CSS color name or hex code (e.g. cornflowerblue or #6495ED). Leave blank for default.'
            ),
        ),
    ]
