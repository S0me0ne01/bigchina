from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core import validators
from django.core.validators import FileExtensionValidator


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset = Category.objects.all(), label = "Категория", empty_label = None, error_messages={'required': 'Выберите категорию'}, widget=forms.widgets.Select(attrs={'size': 8}))
    country = forms.ModelChoiceField(queryset = Country.objects.all(), label = "Страны", empty_label = None, error_messages={'required': 'Выберите страну'}, widget=forms.widgets.Select(attrs={'size': 8}))

    name = forms.CharField(label = 'Название на русском')
    name_kz = forms.CharField(label = 'Название на казахском')
    image = forms.ImageField(label = 'Изображение', validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension' : 'Этот формат не поддерживается', 'required' : ''}, required = True)
    image_2 = forms.ImageField(label = 'Изображение 2', validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension' : 'Этот формат не поддерживается', 'required' : ''}, required = False)
    image_3 = forms.ImageField(label = 'Изображение 3', validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension' : 'Этот формат не поддерживается', 'required' : ''}, required = False)
    video = forms.FileField(label = 'Видео', validators=[validators.FileExtensionValidator( allowed_extensions=('mp4', 'mov', 'gif', 'webm'))], error_messages={'invalid_extension' : 'Этот формат файлов не поддерживается'}, required = False)

    description = forms.CharField(label = 'Описание на русском', widget=forms.widgets.Textarea())
    description_kz = forms.CharField(label = 'Описание на казахском', widget=forms.widgets.Textarea())
    tags = forms.CharField(label = 'Ключевые слова', widget=forms.widgets.Textarea())

    price = forms.IntegerField(label = 'Цена')
    price_wholesale = forms.IntegerField(label = 'Оптовая цена')
    amount_for_wholesale = forms.IntegerField(label = 'Мин. оптовая партия')
    in_stock = forms.BooleanField(label = 'Есть в наличии', required = False)
    by_preorder = forms.BooleanField(label = 'По предзаказу', required = False)
    optional = forms.BooleanField(label = 'Цена договорная', required = False)

    class Meta:
        model = Product
        fields = ('category', 'name', 'name_kz', 'image', 'image_2', 'image_3', 'video', 'description', 'description_kz', 'tags', 'country', 'price', 'price_wholesale', 'amount_for_wholesale', 'in_stock', 'by_preorder', 'optional')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label = 'Название на русском')
    name_kz = forms.CharField(label = 'Название на казахском')
    image = forms.ImageField(label = 'Изображение', validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension' : 'Этот формат не поддерживается', 'required' : ''}, required = True)

    class Meta:
        model = Category
        fields = ('name', 'name_kz', 'image',)


class SubCategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset = Category.objects.all(), label = "Категория", empty_label = None, error_messages={'required': 'Выберите категорию'}, widget=forms.widgets.Select(attrs={'size': 8}))
    name = forms.CharField(label = 'Название на русском')
    name_kz = forms.CharField(label = 'Название на казахском')
    image = forms.ImageField(label = 'Изображение', validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension' : 'Этот формат не поддерживается', 'required' : ''}, required = True)

    class Meta:
        model = SubCategory
        fields = ('parent', 'name', 'name_kz', 'image',)


class AlertForm(forms.ModelForm):
    text = forms.CharField(label = 'Текст')
    text_kz = forms.CharField(label = 'Текст на казахском')

    class Meta:
        model = Alert
        fields = ('text', 'text_kz',)


class CountryForm(forms.ModelForm):
    name = forms.CharField(label = 'Название на русском')
    name_kz = forms.CharField(label = 'Название на казахском')

    class Meta:
        model = Country
        fields = ('name', 'name_kz',)


class QuantityForm(forms.ModelForm):
    quantity = forms.IntegerField(label = 'Количество')

    class Meta:
        model = Cart
        fields = ('quantity',)


class PhoneForm(forms.ModelForm):
    number = forms.CharField(label = '')

    class Meta:
        model = Phone
        fields = ('number',)


class SearchForm(forms.ModelForm):
    text = forms.CharField(label = '')

    class Meta:
        model = Search
        fields = ('text',)


class LoginForm(forms.Form):
    username = forms.CharField(label = 'Ваш никнейм')
    password = forms.CharField(label = 'Ваш пароль', widget=forms.PasswordInput)
