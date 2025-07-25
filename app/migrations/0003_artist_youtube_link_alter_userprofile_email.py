# Generated by Django 5.2.1 on 2025-06-17 20:02

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_create_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='youtube_link',
            field=models.URLField(blank=True, null=True, validators=[app.models.validate_youtube_url]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
