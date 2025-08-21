from django.http import HttpResponseRedirect
from django.shortcuts import render
from shop.models import CatTransport, Transport, Basket
from users.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def index(request):
    context = {'title': 'Rool Shop', 'username': 'bingo'}
    return render(request, 'shop/index.html', context)


def products(request, category_id=None, page_number=1):
    if category_id:
        category = CatTransport.objects.get(id=category_id)
        transports = Transport.objects.filter(category=category)
    else:
        transports = Transport.objects.all()
    per_page = 12
    paginator = Paginator(transports, per_page)
    transport_paginator = paginator.page(page_number)

    context = {'title': 'Каталог',
               'categories': CatTransport.objects.all(),
               'transports': transport_paginator}
    return render(request, 'shop/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Transport.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
