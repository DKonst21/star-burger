# Generated by Django 4.2.7 on 2023-11-12 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_product_restaurants_alter_orderdetails_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='chosen_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodcartapp.restaurant', verbose_name='Ресторан'),
        ),
    ]
