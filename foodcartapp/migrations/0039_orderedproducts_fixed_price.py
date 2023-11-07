# Generated by Django 4.2.7 on 2023-11-07 18:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_orderdetails_orderedproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproducts',
            name='fixed_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0, 0)]),
        ),
    ]
