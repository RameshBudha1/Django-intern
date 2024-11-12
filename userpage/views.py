from django.shortcuts import render,redirect
from products.models import Products
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from . models import Cart
from django.contrib import messages
from .forms import OrderForm
from .models import Order
from .filters import ProductFilter

# Create your views here.

def home_page(request):
    products = Products.objects.all().order_by('-id')[:8]
    context = {
        'products': products
    }
    return render(request,"client/homepage.html",context)

def product_page(request):
    products = Products.objects.all()
    product_filter = ProductFilter(request.GET,queryset=products)
    product_final = product_filter.qs
    context = {
        'products':product_final,
        'product_filter': product_filter
    }
    return render(request,"client/productpage.html",context)

def product_details_page(request,id):
    product = Products.objects.get(id=id)
    context={
        'product': product
    }
    return render(request,"client/product_details.html",context)

# function to add the items in the cart
@login_required
@user_only
def add_to_cart(request,product_id):
    user = request.user
    product= Products.objects.get(id = product_id)

    check_items_presence = Cart.objects.filter(user=user,product = product)

    if check_items_presence:
        messages.add_message(request,messages.ERROR,"Product already present in the cart")
        return redirect("/product")
    else:
        cart = Cart.objects.create(product=product, user=user)
        if cart:
            messages.add_message(request,messages.SUCCESS,"Item added to the cart")
            return redirect("/mycart")
        else:
            messages.add_message(request,messages.ERROR,"Unable to add item to the cart")
            return redirect("/product")


# function to show the cart items
@login_required
@user_only
def show_cart_items(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items': items
    }
    return render(request,"client/mycart.html",context)

# function to delete cart items
@login_required
@user_only
def delete_cart_items(request,id):
    user = request.user
    items = Cart.objects.filter(user=user,id=id)
    items.delete()
    messages.add_message(request,messages.SUCCESS,"Item removed for cart successfully")
    return redirect('/mycart')

# function to order the items from the cart
@login_required
@user_only
def order_form(request,product_id,cart_id):
    user = request.user
    product = Products.objects.get(id = product_id)
    cart_item = Cart.objects.get(id = cart_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = product.product_price
            total_price = int(quantity) * int(price)
            contact_no = request.POST.get('contact_no')
            address = request.POST.get('address')
            payment_method = request.POST.get('payment_method')
            payment_status = request.POST.get('payment_status')
            status = request.POST.get('status')

            order = Order.objects.create(
                user = user,
                products = product,
                quantity = quantity,
                total_price = total_price,
                contact_no = contact_no,
                address = address,
                payment_method = payment_method,
                payment_status = payment_status,
                status = status,
            )
            if order.payment_method == 'Cash On Delivery':
                cart = Cart.objects.get(id = cart_id)
                cart.delete()
                messages.add_message(request,messages.SUCCESS,"Order successful")
                return redirect("/myorder")
            elif order.payment_method == 'Esewa':
                context = {
                    'order':order,
                    'cart':cart_item
                }
                return render(request,"client/esewa_payment.html",context)
            else:
                messages.add_message(request,messages.ERROR,"Something went wrong")
                return render(request,"client/order-form.html",{'form':form})
        
    context = {
        'form': OrderForm
    }
    return render(request,"client/order-form.html",context)

@login_required
@user_only
def show_order_items(request):
    user = request.user
    items = Order.objects.filter(user=user)
    context = {
        'items' : items,
    }
    return render(request,"client/myorder.html",context)

import requests as req
def esewa_verify(request):
    import xml.etree.ElementTree as ET
    oid = request.GET.get('oid')
    amount = request.GET.get('amt')
    refId = request.GET.get('refId')
    url = "https://uat.esewa.com.np/epay/transrec"
    d = {
    'amt': amount,
    'scd': 'EPAYTEST',
    'rid': refId,
    'pid': oid,
    }
    resp = req.post(url,d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == 'Success':
        order_id = oid.split("_")[0]
        order = Order.objects.get(id = order_id)
        order.payment_status = True
        order.save()
        cart_id = oid.split("_")[1]
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        messages.add_message(request,messages.SUCCESS,"Payment successful")
        return redirect('/myorder')
    else:
        messages.add_message(request,messages.ERROR,"Unable to make payment")
        return redirect('/mycart')
    
