# Generated by Django 4.2.2 on 2023-06-09 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_zadaniastale_alter_room_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='zadaniastale',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zadaniastale',
            name='host',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hosted_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='zadaniastale',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.RemoveField(
            model_name='zadaniastale',
            name='recipients',
        ),
        migrations.AddField(
            model_name='zadaniastale',
            name='recipients',
            field=models.ManyToManyField(limit_choices_to={'Email address': 'pracownik@mail.com'}, to=settings.AUTH_USER_MODEL),
        ),
    ]
