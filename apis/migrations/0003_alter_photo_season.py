# Generated by Django 4.1.7 on 2023-04-08 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_rename_ismainphoto_photo_is_main_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='season',
            field=models.IntegerField(default=0),
        ),
    ]
