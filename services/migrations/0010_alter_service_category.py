# Generated by Django 3.2.11 on 2022-01-07 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Food'), (2, 'Music'), (3, 'Education'), (4, 'Arts'), (5, 'Entertainment'), (6, 'Technical'), (7, 'Craftsmanship'), (8, 'Repair and maintenance'), (9, 'Sports')], default=1, verbose_name='Service category'),
        ),
    ]