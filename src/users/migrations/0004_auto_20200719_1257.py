# Generated by Django 3.0.8 on 2020-07-19 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200719_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='user', max_length=128, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='01000000000', max_length=11, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(default='A', max_length=2, verbose_name='user type'),
        ),
    ]
