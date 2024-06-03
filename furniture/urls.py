from django.urls import path
from . import views

app_name = "furniture"
urlpatterns = [
    path('', views.index, name="index"),
    path('product/view/<int:pk>/', views.detail_product, name="detail_product"),
    path('add/cart/<int:pk>/', views.add_cart, name="add_cart"),
    path('view/cart/',views.view_cart,name='cart_view'),
    path('remove-product/<int:pk>/', views.remove_product, name='remove_product'),
    path('category/<int:pk>/', views.category_view, name='category_view'),
    path('search/', views.search_results, name='search_results'),
    path('about/', views.about, name='about'),
    path('send-order-email/', views.send_order_email, name='send_order_email'),

]
