# Generated by Django 5.0.3 on 2024-03-30 01:02

import pages.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_medication_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='image',
            field=models.ImageField(default='/image.jpg', upload_to=pages.models.generate_unique_filename),
        ),
    ]
