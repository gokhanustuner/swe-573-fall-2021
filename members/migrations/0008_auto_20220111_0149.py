# Generated by Django 3.2.11 on 2022-01-11 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_alter_memberprofile_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]