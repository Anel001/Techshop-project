from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart
from django.conf import settings
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    product.in_cart = True
    product.save()
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=int(request.POST['quantity']),
                 update_quantity=cd['update'])
    return redirect('../')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    product.in_cart = False
    product.save()
    cart.remove(product)
    return redirect('../')


def cart_detail(request):
    cart = Cart(request)
    session = request.session
    cart2 = session.get(settings.CART_SESSION_ID)
    return render(request, 'cart/cart_details.html', {'cart': cart,
                                                      'cart2': cart2})
