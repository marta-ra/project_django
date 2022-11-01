from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .services import CandyServices, OrderServices, CategoryServices
from .utils import Utils
from accounts.services import AccountsServices
from .forms import AddCandyAmount, Order


@require_http_methods(["GET"])
def main(request):
    categories = CategoryServices.get_categories()
    context = {'categories': categories}
    return render(request, 'main.html', context)


@require_http_methods(["GET"])
def candy_show(request, category_id):
    form = AddCandyAmount()
    category = CategoryServices.get_category(category_id)
    candies = CandyServices.get_candies_by_category(category)
    context = {'candies': candies, 'form': form, 'category': category}
    return render(request, 'candies.html', context)


@require_http_methods(["GET"])
def order_show(request):
    order = OrderServices.get_or_create_order(request.user, request.session.get('order_id'))
    order_candies_with_price = CandyServices.get_candies_with_price(order.id)
    total_price = CandyServices.get_sum_order(order_candies_with_price)
    if request.user.is_authenticated:
        default_values = {'firstname': request.user.first_name, 'email': request.user.email,
                          'lastname': request.user.last_name, 'phone': request.user.users_profile.phone,
                          'total_price': total_price, 'order_candies_with_price': order_candies_with_price}
        form = Order(default_values)
    else:
        form = Order()
    context = {'form': form, 'total_price': total_price, 'order_candies_with_price': order_candies_with_price,
               'time_allow': Utils.check_time()}
    return render(request, 'order.html', context)


@require_http_methods(["POST"])
def order_confirm(request, ):
    form = Order(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        order_id = OrderServices.get_or_create_order(request.user, request.session.get('order_id')).id
        order = OrderServices.update_order(order_id, data)
        order_candies_with_price = CandyServices.get_candies_with_price(order_id)
        total_price = CandyServices.get_sum_order(order_candies_with_price)
        context = {'order': order, 'total_price': total_price, 'order_candies_with_price': order_candies_with_price}

        AccountsServices.email_send(data['email'], total_price, order_candies_with_price)
        return render(request, 'order_confirmed.html', context)


@require_http_methods(["POST"])
def add_candy(request, candy_id, category_id):
    form = AddCandyAmount(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        amount = data['amount']
        candy = CandyServices.get_candy(candy_id)
        order = OrderServices.get_or_create_order(request.user, request.session.get('order_id'))
        if not request.user.is_authenticated:
            Utils.session_data(request, order.id)
        CandyServices.create_candy_amount(order, candy, amount)
        return redirect(candy_show, category_id=category_id)


@require_http_methods(["POST"])
def update_candy_amount(request, candy_amount_id):
    quantity = request.POST['quantity']
    CandyServices.update_candy_amount(candy_amount_id, quantity)
    return redirect(order_show)




