# Generated by Django 3.2.11 on 2022-01-08 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0019_service_delivered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerate',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='Attended service'),
        ),
        migrations.AlterField(
            model_name='servicerate',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member attending to the service'),
        ),
    ]