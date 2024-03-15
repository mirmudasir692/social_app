# Generated by Django 5.0.3 on 2024-03-14 06:01

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, validators=[accounts.models.ValidationClass.validate_email]),
        ),
    ]
