# Generated by Django 4.1.7 on 2023-03-05 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_image",
            field=models.ImageField(default="", upload_to="accounts/images"),
        ),
    ]