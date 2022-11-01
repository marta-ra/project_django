from candy.models import Order


class OrderServices:

    @staticmethod
    def get_order(order_id):
        return Order.objects.get(pk=order_id)

    @staticmethod
    def get_in_progress_order_for_user(user):
        return Order.objects.filter(user=user, status=Order.IN_PROGRESS).first()

    @staticmethod
    def create_order_row_auth(user):
        firstname = user.first_name
        lastname = user.last_name
        email = user.email
        return Order.objects.create(firstname=firstname, lastname=lastname, email=email,
                                    status=Order.IN_PROGRESS, user=user)

    @staticmethod
    def create_order_row_not_auth():
        return Order.objects.create(status=Order.IN_PROGRESS)

    @staticmethod
    def get_or_create_order(user, order_id):
        if user.is_authenticated:
            if order := OrderServices.get_in_progress_order_for_user(user):
                pass
            else:
                order = OrderServices.create_order_row_auth(user)
        else:
            if order_id is not None:
                order = OrderServices.get_order(order_id)
            else:
                order = OrderServices.create_order_row_not_auth()
        return order

    @staticmethod
    def update_order(order_id, data):
        order = OrderServices.get_order(order_id)
        order.firstname = data['firstname']
        order.lastname = data['lastname']
        order.email = data['email']
        order.delivery_time = data['delivery_time']
        order.address = data['address']
        order.phone = data['phone']
        order.status = Order.DELIVERY
        order.comment = data['comment']
        order.save()
        return order
