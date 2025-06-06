from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
from .views import cart_add, subscribe_view

urlpatterns = [
    path('', views.home, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('thankyou/', views.thankyou, name='thankyou'),

    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog, name='blog'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),

    path('account/', views.account_view, name='account'),

    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register_view, name='register'),

    path('subscribe/', subscribe_view, name='subscribe'),
]
