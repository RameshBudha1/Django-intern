from django.urls import path
from . import views

urlpatterns = [
    path('product/',views.show_products, name='products'),
    path('category/',views.show_category, name='category'),
    path('addCategory/',views.post_category, name='add_category'),
    path('addProduct/',views.post_product, name='add_products'),
    path('deleteCategory/<int:category_id>',views.delete_category, name="delete_category"),
    path('updateCategory/<int:category_id>',views.update_category, name= 'update_category'),
    path('deleteProduct/<int:product_id>',views.delete_product, name="delete_product"),
    path('updateProduct/<int:product_id>',views.update_product,name = "update_product"),
]