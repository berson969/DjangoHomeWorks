# Generated by Django 4.1 on 2022-09-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='phone',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
