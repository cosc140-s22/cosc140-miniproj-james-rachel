# Generated by Django 4.0.4 on 2022-05-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castlefinder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='castle',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]