from django.urls import path

from . import views

urlpatterns = [
    path('',views.home_page, name="homepage"),
    path('product/',views.product_page , name = "productpage"),
    path('product/<int:id>',views.product_details_page,name="product_detail"),
    path('add_to_cart/<int:product_id>',views.add_to_cart, name="my_cart"),
    path('mycart/',views.show_cart_items, name="show_cart_items"),
    path('delete_cart_items/<int:id>',views.delete_cart_items, name="delete_cart_items"),
    path('order_form/<int:product_id>/<int:cart_id>',views.order_form, name = 'order'),
    path('myorder/',views.show_order_items, name = "my-order"),
    path('esewa_verify/',views.esewa_verify),
]