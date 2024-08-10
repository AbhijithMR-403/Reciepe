# Generated by Django 5.0.7 on 2024-08-09 17:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reciepeapp", "0017_alter_order_order_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="Ingredients",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="Instructions",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="time",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
