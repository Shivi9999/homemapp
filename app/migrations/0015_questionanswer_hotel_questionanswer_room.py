# Generated by Django 4.2.1 on 2024-01-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_add_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionanswer',
            name='hotel',
            field=models.ManyToManyField(to='app.add_hotel'),
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='room',
            field=models.ManyToManyField(to='app.add_room'),
        ),
    ]
