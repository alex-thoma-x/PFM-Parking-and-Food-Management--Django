# Generated by Django 4.0.4 on 2022-06-16 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_item_rid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='city',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='approved',
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_addr',
            field=models.IntegerField(blank=True, default=-1),
        ),
    ]
