# Generated by Django 4.2.2 on 2023-06-09 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_topic_room_host_message_room_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZadaniaStale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('recipients', models.CharField(choices=[('all', 'All Users'), ('selected', 'Selected User')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]