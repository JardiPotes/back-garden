# Generated by Django 4.1.1 on 2022-09-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentications', '0004_users_has_garden_users_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
