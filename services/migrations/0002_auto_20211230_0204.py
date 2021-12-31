# Generated by Django 3.2.10 on 2021-12-30 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date'),
        ),
        migrations.CreateModel(
            name='ServiceRate',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Service rate ID')),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, 'Terrible'), (2, 'Bad'), (3, 'Neutral'), (4, 'Good'), (5, 'Excellent')], verbose_name='Service rate value')),
                ('content', models.TextField(verbose_name='Member comment for service')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='Attended service')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member attending to the service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAttendanceRequest',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Service attendance request ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Approved'), (2, 'Declined'), (3, "Waiting for service owner's approval")], default=3, verbose_name='Service attendance request status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member requesting to attend to the service')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='Service requested to attend')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAttendance',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Service attendance ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Active'), (2, 'Cancelled')], default=1, verbose_name='Service attendance status')),
                ('date', models.DateTimeField(verbose_name='Start date')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Member attending to the service')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='Attended service')),
            ],
        ),
    ]
