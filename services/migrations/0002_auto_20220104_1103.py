# Generated by Django 3.2.10 on 2022-01-04 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Service owner'),
        ),
        migrations.AlterField(
            model_name='serviceattendance',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member attending to the service'),
        ),
        migrations.AlterField(
            model_name='serviceattendance',
            name='service',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='Attended service'),
        ),
        migrations.AlterField(
            model_name='serviceattendancerequest',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member requesting to attend to the service'),
        ),
        migrations.AlterField(
            model_name='serviceattendancerequest',
            name='service',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='Service requested to attend'),
        ),
        migrations.AlterField(
            model_name='servicerate',
            name='service',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='Attended service'),
        ),
        migrations.AlterField(
            model_name='servicerate',
            name='voter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member attending to the service'),
        ),
    ]
