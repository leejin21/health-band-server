# Generated by Django 3.0.8 on 2020-10-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wearerData', '0003_auto_20201024_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wearerdata',
            name='nowDate',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='nowTime'),
        ),
        migrations.AlterField(
            model_name='wearerdata',
            name='nowTime',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='nowTime'),
        ),
        migrations.AlterField(
            model_name='wearermeter',
            name='nowDT',
            field=models.DateTimeField(auto_now=True, verbose_name='now date time'),
        ),
    ]