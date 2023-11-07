from django.db import models

from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.shortcuts import get_object_or_404
from django.http import Http404

from django.db.models.signals import pre_save, post_save, post_init
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

import datetime


class Product(models.Model):
    name = models.CharField(max_length = 1000)
    name_kz = models.CharField(max_length = 1000, null = True, blank = True)
    description = models.TextField()
    description_kz = models.TextField(null = True, blank = True)
    tags = models.CharField(max_length = 1000, null = True, blank = True)
    image = models.ImageField(verbose_name = 'Изображение', null = True, blank = True)
    image_2 = models.ImageField(verbose_name = 'Изображение 2', null = True, blank = True)
    image_3 = models.ImageField(verbose_name = 'Изображение 3', null = True, blank = True)
    video = models.FileField(upload_to='video/', null = True, blank = True)

    price = models.PositiveIntegerField()
    price_wholesale = models.PositiveIntegerField(default = 0)
    amount_for_wholesale = models.PositiveIntegerField(default = 0)
    discount = models.PositiveIntegerField(default = 0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    in_stock = models.BooleanField(default = True)
    by_preorder = models.BooleanField(default = False)
    optional = models.BooleanField(default = False)

    category = models.ForeignKey('Category', related_name = 'category', on_delete = models.CASCADE)
    country = models.ForeignKey('Country', related_name = 'country', on_delete = models.CASCADE)

    views = models.PositiveIntegerField(default = 0)
    published = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

@receiver(pre_save, sender = Product)
def find_discount(sender, instance, **kwargs):
    try:
        obj = get_object_or_404(sender, id = instance.pk)
    except Http404:
        pass
    else:
        if not obj.price == instance.price:
            if instance.price > obj.price:
                instance.discount = 0
            else:
                instance.discount = 100 - (100 * (instance.price / obj.price))


class Category(models.Model):
    name = models.CharField(max_length = 1000)
    name_kz = models.CharField(max_length = 1000)
    image = models.ImageField(verbose_name = 'Изображение', null = True, blank = True)

    def __str__(self):
        return self.name


class SubCategory(Category):
    parent = models.ForeignKey('Category', related_name = 'parent_category', on_delete = models.CASCADE)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length = 1000)
    name_kz = models.CharField(max_length = 1000)

    def __str__(self):
        return self.name
    

class Alert(models.Model):
    text = models.TextField()
    text_kz = models.TextField()

    def __str__(self):
        return self.text


class Cart(models.Model):
    user = models.ForeignKey(User, null= True, blank = True, related_name = 'cart', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null = True, blank = True, related_name = 'product', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return self.product.name + ' ' + str(self.quantity)


class Phone(models.Model):
    number = models.CharField(max_length = 20)

    def __str__(self):
        return self.number


class Ip(models.Model):
    adress = models.CharField(max_length = 50)
    products = models.TextField(default = '')

    def __str__(self):
        return self.adress


class Visit(models.Model):
    year = models.PositiveIntegerField(default = 0)
    month = models.PositiveIntegerField(default = 0)
    visits = models.PositiveIntegerField(default = 0)
    from_kz = models.PositiveIntegerField(default = 0)
    from_other = models.PositiveIntegerField(default = 0)
    visited = models.TextField(default = '', null = True)

    def __str__(self):
        return str(self.year) + ' ' + str(self.month)

@receiver(pre_save, sender = Visit)
def visit_save(sender, instance, **kwargs):
    instance.year = datetime.datetime.now().year
    instance.month = datetime.datetime.now().month


class Search(models.Model):
    text = models.CharField(max_length = 100)
