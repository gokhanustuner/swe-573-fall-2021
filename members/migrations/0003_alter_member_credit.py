# Generated by Django 3.2.10 on 2022-01-05 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_memberprofile_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='credit',
            field=models.PositiveIntegerField(blank=True, default=5, null=True),
        ),
    ]
