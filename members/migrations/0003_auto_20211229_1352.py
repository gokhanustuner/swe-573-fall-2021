# Generated by Django 3.2.10 on 2021-12-29 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20211229_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='credit',
            field=models.PositiveIntegerField(default=20, verbose_name='Total credits'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=500, null=True, verbose_name='Phone number'),
        ),
    ]
