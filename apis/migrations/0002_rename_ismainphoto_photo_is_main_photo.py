# Generated by Django 4.1.7 on 2023-04-08 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apis", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="photo",
            old_name="isMainPhoto",
            new_name="is_main_photo",
        ),
    ]
