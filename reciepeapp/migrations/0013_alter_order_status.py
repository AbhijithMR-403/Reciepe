# Generated by Django 5.0.7 on 2024-08-06 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reciepeapp", "0012_rename_created_at_order_order_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                ],
                default="Pending",
                max_length=50,
            ),
        ),
    ]
