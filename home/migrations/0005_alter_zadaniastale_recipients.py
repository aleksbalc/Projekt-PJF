# Generated by Django 4.2.2 on 2023-06-09 21:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_zadaniastale_description_zadaniastale_host_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zadaniastale',
            name='recipients',
            field=models.ManyToManyField(limit_choices_to={'email': 'pracownik@mail.com'}, to=settings.AUTH_USER_MODEL),
        ),
    ]
