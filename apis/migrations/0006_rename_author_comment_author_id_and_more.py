# Generated by Django 4.1.7 on 2023-03-24 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0005_alter_comment_author_alter_comment_receiver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='author_id',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='receiver',
            new_name='receiver_id',
        ),
    ]
