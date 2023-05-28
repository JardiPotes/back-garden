# Generated by Django 4.1.7 on 2023-05-19 14:25

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis", "0006_alter_comment_created_at_alter_comment_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 19, 14, 25, 3, 391845, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="updated_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 19, 14, 25, 3, 391850, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="garden",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 19, 14, 25, 3, 391399, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="garden",
            name="updated_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 19, 14, 25, 3, 391537, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="sent_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 19, 14, 25, 3, 392117, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
