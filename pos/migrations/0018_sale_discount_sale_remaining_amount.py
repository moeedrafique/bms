# Generated by Django 4.2.7 on 2023-12-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0017_customer_sale_saleitem_sale_products_sale_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='sale',
            name='remaining_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
