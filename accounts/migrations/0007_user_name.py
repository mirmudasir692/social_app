# Generated by Django 5.0.3 on 2024-03-17 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
    ]
