# Generated by Django 3.0.8 on 2020-08-08 13:59

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200808_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmpw',
            field=models.CharField(default='0000', max_length=128, verbose_name='confirmpw'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null='user78165', unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
