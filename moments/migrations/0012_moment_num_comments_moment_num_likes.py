# Generated by Django 5.0.3 on 2024-05-14 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moments", "0011_moment_cover_pic"),
    ]

    operations = [
        migrations.AddField(
            model_name="moment",
            name="num_comments",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="moment", name="num_likes", field=models.IntegerField(default=0),
        ),
    ]
