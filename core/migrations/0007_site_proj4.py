from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_geojson_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='proj4',
            field=models.CharField(
                'Proj.4',
                max_length=500,
                blank=True,
                default='',
                help_text='Proj.4 string for this site, e.g. +proj=lcc +lat_0=39.3333333333333 +lon_0=-77.75 +lat_1=40.9666666666667 +lat_2=39.9333333333333 +x_0=600000 +y_0=0 +ellps=GRS80 +nadgrids=us_noaa_pahpgn.tif +units=us-ft +no_defs +type=crs',
            ),
        ),
    ]
