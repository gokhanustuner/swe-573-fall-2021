# Generated by Django 3.2.10 on 2022-01-04 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Event owner'),
        ),
        migrations.AlterField(
            model_name='eventattendancerequest',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='Event requested to attend'),
        ),
        migrations.AlterField(
            model_name='eventattendancerequest',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member requesting to attend to the event'),
        ),
        migrations.AlterField(
            model_name='eventrate',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='Attended event'),
        ),
        migrations.AlterField(
            model_name='eventrate',
            name='voter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member attending to the event'),
        ),
    ]
