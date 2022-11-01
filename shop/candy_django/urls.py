"""candy_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from candy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('candy_show<str:category_id>', views.candy_show, name='candy_show'),
    path('add_candy<str:candy_id><str:category_id>', views.add_candy, name='add_candy'),
    path('update_candy_amount<str:candy_amount_id>', views.update_candy_amount, name='update_candy_amount'),
    path('order', views.order_show, name='order_show'),
    path('order_confirm', views.order_confirm, name='order_confirm'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]
