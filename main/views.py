from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, UserManager
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import *

import time
import datetime
import requests
import telegram

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse

from django.template import RequestContext

from django.core.paginator import Paginator
from django.core.mail import send_mail


def homepage(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    categories = Category.objects.filter(subcategory__isnull = True)
    products = Product.objects.order_by('-published')[:9]
    alert = Alert.objects.get(id = 1)

    adress = request.META.get('HTTP_X_FORWARDED_FOR')
    if adress:
        ip = adress.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        visit = get_object_or_404(Visit, year = datetime.datetime.now().year, month = datetime.datetime.now().month)
        if ip not in visit.visited:
            visit.visited = visit.visited + ' ' + ip
            visit.visits += 1
            visit.save()
    except Http404:
        Visit.objects.create(visited = ip, visits = 1)

    context = {'language' : language, 'categories' : categories, 'products' : products, 'alert' : alert}
    return render(request, 'homepage.html', context)


def all(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    categories = Category.objects.all()
    products = Product.objects.order_by('-published')

    paginator = Paginator(products, 9)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'language' : language, 'categories' : categories, 'products' : page.object_list, 'page' : page}
    return render(request, 'all.html', context)


def categories(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    categories = Category.objects.all()

    context = {'language' : language, 'categories' : categories}
    return render(request, 'categories.html', context)


def sort_by(request, kind, sort):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    categories = Category.objects.all()
    if kind == 'category':
        sort = get_object_or_404(Category, name = sort)
        subs = SubCategory.objects.filter(parent = sort)
        products = Product.objects.filter(category = sort).order_by('-published')
    elif kind == 'country':
        sort = get_object_or_404(Country, name = sort)
        subs = None
        products = Product.objects.filter(country = sort).order_by('-published')
    else:
        return HttpResponseNotFound()

    paginator = Paginator(products, 9)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'language' : language, 'categories' : categories, 'sort' : sort, 'subs' : subs, 'kind' : kind, 'products' : page.object_list, 'page' : page}
    return render(request, 'sort_by.html', context)


def detail(request, product_id):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    categories = Category.objects.all()
    product = get_object_or_404(Product, id = product_id)

    context = {'language' : language, 'categories' : categories, 'product' : product}
    return render(request, 'detail.html', context)


def add(request, kind):
    if request.user.is_staff:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        categories = Category.objects.all()

        if kind == 'product':
            form_type = ProductForm
        elif kind == 'category':
            form_type = CategoryForm
        elif kind == 'sub_category':
            form_type = SubCategoryForm
        elif kind == 'country':
            form_type = CountryForm
        else:
            context = {'language' : language, 'categories' : categories}
            return render(request, 'add_choose.html', context)

        if request.method == "POST":
            f = form_type(request.POST, request.FILES)
            if f.is_valid():
                f = f.save(commit = False)
                f.save()
                return HttpResponseRedirect(reverse('main:all', args = ()))
            else:
                context = {'language' : language, 'categories' : categories, 'kind' : kind, 'form' : f}
                return render(request, 'add.html', context)
        else:
            f = form_type()
            context = {'language' : language, 'categories' : categories, 'kind' : kind, 'form' : f}
            return render(request, 'add.html', context)
    else:
        return HttpResponseNotFound()


def edit(request, kind, object_id):
    if request.user.is_staff:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        categories = Category.objects.all()

        if kind == 'product':
            form_type = ProductForm
            object = get_object_or_404(Product, id = object_id)
        elif kind == 'category':
            form_type = CategoryForm
            object = get_object_or_404(Category, id = object_id)
        elif kind == 'sub_category':
            form_type = SubCategoryForm
            object = get_object_or_404(SubCategory, id = object_id)
        elif kind == 'country':
            form_type = CountryForm
            object = get_object_or_404(Country, id = object_id)
        elif kind == 'alert':
            form_type = AlertForm
            object = get_object_or_404(Alert, id = 1)
        else:
            context = {'language' : language, 'categories' : categories}
            return render(request, 'edit.html', context)

        if request.method == "POST":
            f = form_type(request.POST, request.FILES, instance = object)
            if f.is_valid():
                f = f.save(commit = False)
                f.save()
                if kind == 'product':
                    return HttpResponseRedirect(reverse('main:detail', args = (object_id,)))
                else:
                    return HttpResponseRedirect(reverse('main:all', args = ()))
            else:
                context = {'language' : language, 'categories' : categories, 'kind' : kind, 'form' : f}
                return render(request, 'edit.html', context)
        else:
            f = form_type(instance = object)
            context = {'language' : language, 'categories' : categories, 'kind' : kind, 'form' : f}
            return render(request, 'edit.html', context)
    else:
        return HttpResponseNotFound()


def delete(request, kind, object_id):
    if request.user.is_staff:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        if kind == 'product':
            object = get_object_or_404(Product, id = object_id)

        elif kind == 'category':
            object = get_object_or_404(Category, id = object_id)

        elif kind == 'country':
            object = get_object_or_404(Country, id = object_id)

        else:
            return HttpResponseNotFound()

        if kind == 'product':
            if object.image:
                object.image.delete()
        object.delete()

        return HttpResponseRedirect(reverse('main:all', args = ()))
    else:
        return HttpResponseNotFound


def search(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    text = request.GET.get('input')

    categories = Category.objects.all()
    products = Product.objects.filter(Q(name__icontains = text) | Q(tags__icontains = text))

    context = {'language' : language, 'categories' : categories, 'products' : products}
    return render(request, 'search_result.html', context)


def cart(request):
    if request.user.is_authenticated:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        categories = Category.objects.all()
        carts = Cart.objects.filter(user = request.user)

        context = {'language' : language, 'categories' : categories, 'carts' : carts}
        return render(request, 'cart.html', context)
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def to_cart(request, product_id):
    if request.user.is_authenticated:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        categories = Category.objects.all()
        quantity = request.GET.get('input')

        product = get_object_or_404(Product, id = product_id)
        try:
            cart = get_object_or_404(Cart, user = request.user, product = product)
            if quantity != None:
                cart.quantity = quantity
            else:
                cart.quantity = 1
            cart.save()
        except Http404:
            Cart.objects.create(user = request.user, product = product, quantity = 1)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def from_cart(request, product_id):
    if request.user.is_authenticated:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        product = get_object_or_404(Product, id = product_id)
        cart = Cart.objects.get(user = request.user, product = product)
        cart.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def cart_erase(request):
    if request.user.is_authenticated:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        carts = Cart.objects.filter(user = request.user)
        for cart in carts:
            cart.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def phone(request, product_id, phone):
    categories = Category.objects.all()
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if phone:
        if request.user.is_authenticated and product_id == '-1':
            message = 'Клиент с номером ' + phone + ' хочет приобрести '
            carts = Cart.objects.filter(user = request.user)
            for cart in carts:
                message = message + cart.product.name + ' ' + str(cart.quantity) + ' шт. '
        else:
            product = get_object_or_404(Product, id = product_id)
            message = 'Клиент с номером ' + phone + ' хочет приобрести ' + product.name

        telegram_bot_sendtext(message)
        return redirect(request.META['HTTP_REFERER'])
    else:
        if request.method == "POST":
            pf = PhoneForm(request.POST)
            if pf.is_valid():
                pf = pf.save(commit=False)
                phone = pf.number
                return HttpResponseRedirect(reverse('main:phone', args=(product_id, phone,)))
            else:
                context = {'language' : language, 'form' : pf, 'product_id' : product_id, 'categories' : categories}
                return render(request, 'phone.html', context)
        else:
            pf = PhoneForm()
            context = {'language' : language, 'form': pf, 'product_id' : product_id, 'categories' : categories}
            return render(request, 'phone.html', context)


def telegram_bot_sendtext(bot_message):
    bot_token = '1800514857:AAHurdDky_Rz8_5RVhOhUR4cVRE3YhAngc4'
    bot_chatID = '-1001189121314'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


def language_change(request, new_language):
    response = redirect(request.META['HTTP_REFERER'])
    if new_language == 'kz' or new_language == 'ru':
        response.set_cookie('language', new_language)

    return response


def statistics(request):
    if request.user.is_staff:
        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        categories = Category.objects.all()
        visits = Visit.objects.order_by('-year', '-month')

        context = {'language' : language, 'categories' : categories, 'visits' : visits, 'lang' : language}
        return render(request, 'statistics.html', context)
    else:
        return HttpResponseNotFound()


def user_login(request):
    categories = Category.objects.all()
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            cd = lf.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main:homepage', args = ()))
                else:
                    return HttpResponse('Ошибка аккаунта')
            else:
                return HttpResponse('Некорректные данные')
        else:
            context = {'categories' : categories, 'language' : language, 'form' : lf}
            return render(request, 'login.html', context)
    else:
        lf = LoginForm()
        context = {'categories' : categories, 'language' : language, 'form' : lf}
        return render(request, 'login.html', context)


def register(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    categories = Category.objects.all()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:login', args=()))
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'language' : language, 'form' : form, 'categories' : categories})
