# Generated by Django 4.1.1 on 2022-12-12 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('zipcode', models.CharField(max_length=5)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photoUrl', models.URLField(max_length=300)),
                ('isMainPhoto', models.BooleanField()),
                ('season', models.IntegerField()),
                ('gardenId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.garden')),
            ],
        ),
    ]
