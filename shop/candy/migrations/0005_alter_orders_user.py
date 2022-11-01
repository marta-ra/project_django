# Generated by Django 4.0.3 on 2022-03-10 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candy', '0004_alter_orders_delivery_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_order', to=settings.AUTH_USER_MODEL),
        ),
    ]
