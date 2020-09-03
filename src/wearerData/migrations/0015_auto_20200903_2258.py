# Generated by Django 3.0.8 on 2020-09-03 22:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wearerData', '0014_auto_20200903_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wearerdata',
            name='nowTime',
            field=models.TimeField(default=datetime.time(22, 58, 21, 475498), null=True, verbose_name='nowTime'),
        ),
        migrations.CreateModel(
            name='WearerEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nowDate', models.DateField(default=datetime.date(2020, 9, 3), null=True, verbose_name='nowTime')),
                ('nowTime', models.TimeField(default=datetime.time(22, 58, 21, 476031), null=True, verbose_name='nowTime')),
                ('fallEvent', models.BooleanField(default=False, null=True)),
                ('heartEvent', models.BooleanField(default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]