# Generated by Django 3.2.11 on 2022-01-05 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='events'),
        ),
    ]
