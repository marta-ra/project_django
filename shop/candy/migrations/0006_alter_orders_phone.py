# Generated by Django 4.0.3 on 2022-03-10 15:51

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('candy', '0005_alter_orders_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]