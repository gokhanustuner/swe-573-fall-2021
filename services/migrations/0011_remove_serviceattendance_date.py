# Generated by Django 3.2.11 on 2022-01-07 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_alter_service_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceattendance',
            name='date',
        ),
    ]