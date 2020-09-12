# Generated by Django 3.0.8 on 2020-09-11 22:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wearerData', '0020_auto_20200911_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wearerdata',
            name='nowTime',
            field=models.TimeField(default=datetime.time(22, 22, 27, 321461), null=True, verbose_name='nowTime'),
        ),
        migrations.AlterField(
            model_name='wearerevent',
            name='nowTime',
            field=models.TimeField(default=datetime.time(22, 22, 27, 322540), null=True, verbose_name='nowTime'),
        ),
        migrations.CreateModel(
            name='WearerPreEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prevHeat', models.CharField(default='N', max_length=1, null=True)),
                ('firstHeat', models.DateTimeField(default=datetime.datetime(2020, 9, 11, 22, 22, 27, 322159))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
