# Generated by Django 4.2.2 on 2023-06-10 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_zadaniastale_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zadaniastale',
            name='progress',
            field=models.CharField(choices=[('przydzielone', 'Przydzielone'), ('rozpoczęte', 'Rozpoczęte'), ('zakończone', 'Zakończone')], default='przydzielone', max_length=20, null=True),
        ),
    ]
