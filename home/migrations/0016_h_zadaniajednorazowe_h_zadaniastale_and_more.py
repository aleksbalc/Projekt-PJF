# Generated by Django 4.2.2 on 2023-06-11 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0015_zadaniastale_created_zadaniastale_updated_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='H_ZadaniaJednorazowe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateField(blank=True, null=True)),
                ('finished', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='H_ZadaniaStale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateField(blank=True, null=True)),
                ('finished', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrzydzieloneZadanieStale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('started', models.DateField(blank=True, null=True)),
                ('finished', models.DateField(blank=True, null=True)),
                ('host', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hosted_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='host',
        ),
        migrations.RemoveField(
            model_name='room',
            name='topic',
        ),
        migrations.AlterModelOptions(
            name='zadaniajednorazowe',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveField(
            model_name='zadaniajednorazowe',
            name='progress',
        ),
        migrations.RemoveField(
            model_name='zadaniajednorazowe',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='zadaniastale',
            name='created',
        ),
        migrations.RemoveField(
            model_name='zadaniastale',
            name='host',
        ),
        migrations.RemoveField(
            model_name='zadaniastale',
            name='progress',
        ),
        migrations.RemoveField(
            model_name='zadaniastale',
            name='recipients',
        ),
        migrations.RemoveField(
            model_name='zadaniastale',
            name='updated',
        ),
        migrations.AddField(
            model_name='zadaniajednorazowe',
            name='finished',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zadaniajednorazowe',
            name='started',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.AddField(
            model_name='przydzielonezadaniestale',
            name='id_zs',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to='home.zadaniastale'),
        ),
        migrations.AddField(
            model_name='przydzielonezadaniestale',
            name='recipient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='received_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='h_zadaniastale',
            name='id_pzs',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.przydzielonezadaniestale'),
        ),
        migrations.AddField(
            model_name='h_zadaniajednorazowe',
            name='id_pzs',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.zadaniajednorazowe'),
        ),
    ]