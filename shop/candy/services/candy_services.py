from django.db.models import Sum, F
from candy.models import Candy, CandyAmount
from .order_services import OrderServices


class CandyServices:

    @staticmethod
    def create_candy_amount(order, candy, quantity):
        return CandyAmount.objects.create(order=order, candy=candy, quantity=quantity)

    @staticmethod
    def get_candies_by_category(category):
        return category.candies.all()

    @staticmethod
    def get_candy(candy_id):
        return Candy.objects.get(pk=candy_id)

    @staticmethod
    def get_candy_amount(candy_amount_id):
        return CandyAmount.objects.get(pk=candy_amount_id)

    @staticmethod
    def get_sum_order(order_candies_with_price):
        total_price = order_candies_with_price.aggregate(total=Sum(F('price')))['total']
        return total_price

    @staticmethod
    def get_candies_with_price(order_id):
        order = OrderServices.get_order(order_id)
        candies_price = order.candy_amounts.all().annotate(price=F('quantity') * F('candy_id__cost'))
        return candies_price

    @staticmethod
    def get_candy_amount_all(order_id):
        order = OrderServices.get_order(order_id)
        return order.candy_amounts.all()

    @staticmethod
    def update_candy_amount(candy_amount_id, quantity):
        candy_amount_obj = CandyServices.get_candy_amount(candy_amount_id)
        candy_amount_obj.quantity = quantity
        candy_amount_obj.save()
