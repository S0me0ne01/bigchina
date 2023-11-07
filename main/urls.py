from django.contrib import admin
from django.urls import path

from .views import *

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'main'

urlpatterns = [
    #Authentication
    path('login/', user_login, name = 'login'),
    path('logout/', LogoutView.as_view(next_page='main:homepage', template_name = "logged_out.html"), name = 'logout'),
    path('register', register, name = 'register'),
    #Homepage
    path('', homepage, name = 'homepage'),
    #All
    path('all/', all, name = 'all'),
    #Sort_by
    path('sort_by/<str:kind>/<str:sort>/', sort_by, name = 'sort_by'),
    #Detail
    path('detail/<str:product_id>/', detail, name = 'detail'),
    #Add|Edit|Delete
    path('add/<str:kind>/', add, name = 'add'),
    path('add/', add, kwargs={'kind': None}, name = 'add'),
    path('edit/<str:kind>/<str:object_id>/', edit, name = 'edit'),
    path('delete/<str:kind>/<str:object_id>/', delete, name = 'delete'),
    #Statistics
    path('statistics/', statistics, name = 'statistics'),
    #Search
    path('search/', search, name = 'search'),
    #Cart
    path('cart/add/<str:product_id>/', to_cart, name = 'to_cart'),
    path('cart/remove/<str:product_id>/', from_cart, name = 'from_cart'),
    path('cart/erase/', cart_erase, name = 'cart_erase'),
    path('cart/', cart, name = 'cart'),
    #Phone
    path('phone/<str:product_id>/<str:phone>/', phone, name = 'phone'),
    path('phone/<str:product_id>/', phone, kwargs={'phone': None}, name = 'phone'),
    #Language
    path('language/change/<str:new_language>/', language_change, name = 'language_change'),
]
