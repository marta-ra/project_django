from django.db import models
from django.conf import settings


class Category(models.Model):
    category = models.CharField(max_length=255)


class Candy(models.Model):
    candy = models.CharField(max_length=255)
    cost = models.FloatField()
    category = models.ForeignKey(
            Category,
            on_delete=models.CASCADE,
            related_name='candies'
    )


class Order(models.Model):
    IN_PROGRESS = 'in_progress'
    DELIVERY = 'delivery'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (IN_PROGRESS, 'in_progress'),
        (DELIVERY, 'delivery'),
        (COMPLETED, 'completed'),
    )
    firstname = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='in_progress')
    comment = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='orders',
            null=True,
            blank=True
        )


class CandyAmount(models.Model):
    candy = models.ForeignKey(
            Candy,
            on_delete=models.CASCADE,
            related_name='candy_amounts'
    )
    order = models.ForeignKey(
            Order,
            on_delete=models.CASCADE,
            related_name='candy_amounts'
    )
    quantity = models.FloatField()


class UserProfile(models.Model):
    phone = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='users_profile'
    )
