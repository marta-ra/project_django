# Generated by Django 4.0.3 on 2022-03-10 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candy', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Сandies',
            new_name='Candy',
        ),
        migrations.RenameModel(
            old_name='СandyAmount',
            new_name='CandyAmount',
        ),
        migrations.RenameModel(
            old_name='CandyCategories',
            new_name='Category',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='to_pay',
        ),
        migrations.AlterField(
            model_name='orders',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='orders',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='orders',
            name='delivery_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='orders',
            name='firstname',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='orders',
            name='lastname',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_order', to=settings.AUTH_USER_MODEL),
        ),
    ]
