# Generated by Django 3.0.8 on 2020-08-12 06:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wearerData', '0002_auto_20200812_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wearerdata',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 8, 12, 6, 14, 57, 396903, tzinfo=utc), verbose_name='nowTime'),
        ),
    ]