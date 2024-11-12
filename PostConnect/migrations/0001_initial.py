# Generated by Django 5.0.7 on 2024-10-31 20:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('caption', models.TextField(blank=True, max_length=500)),
                ('image', models.ImageField(upload_to='posts')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('archive', models.BooleanField(default=False)),
                ('num_likes', models.IntegerField(db_default=0, default=0)),
            ],
        ),
    ]
