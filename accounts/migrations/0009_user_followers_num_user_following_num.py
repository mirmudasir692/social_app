# Generated by Django 5.0.3 on 2024-03-25 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers_num',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_num',
            field=models.BigIntegerField(default=0),
        ),
    ]
