# Generated by Django 5.0.3 on 2024-03-24 17:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('moments', '0010_alter_fruit_content'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bucketed_moments', to='moments.moment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_moments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
