# Generated by Django 3.2.11 on 2022-01-11 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_member_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='members/'),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Short bio'),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='personal_characteristics',
            field=models.TextField(blank=True, null=True, verbose_name='Personal characteristics'),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='talents',
            field=models.TextField(blank=True, null=True, verbose_name='Talents'),
        ),
    ]
