# Generated by Django 3.2.10 on 2021-12-29 10:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Event Location ID')),
                ('name', models.CharField(max_length=500, verbose_name='Location name')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('address', models.TextField(verbose_name='Event address')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Event ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_date', models.DateTimeField(verbose_name='Start data')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
                ('repetition_term', models.PositiveSmallIntegerField(choices=[(1, 'One-Time'), (2, 'Weekly'), (3, 'Monthly'), (4, 'Yearly')], default=1, verbose_name='Repetition term')),
                ('privacy_status', models.PositiveSmallIntegerField(choices=[(1, 'Public'), (2, 'Private')], default=1, verbose_name='Privacy status')),
                ('participant_limit', models.PositiveIntegerField(default=0, verbose_name='Participant limit')),
                ('participant_picking', models.PositiveSmallIntegerField(choices=[(1, 'Free'), (2, 'Pick participants')], default=1, verbose_name='Participant picking')),
                ('cancelled', models.BooleanField(choices=[(0, 'No'), (1, 'Yes')], default=0, max_length=1, verbose_name='Cancelled')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventlocation', verbose_name='Location')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member', verbose_name='Event owner')),
            ],
        ),
    ]
