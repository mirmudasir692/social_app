# Generated by Django 5.0.3 on 2024-06-11 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PostConnect", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]