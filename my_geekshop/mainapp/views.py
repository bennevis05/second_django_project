from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.cache import cache_page
from .models import ProductCategory, Product
import random


# class Fact(object):
#     def get_factorial(self):
#         fact = 1
#         for i in range(1, 15000 + 1):
#             fact = fact * i
#         return fact


def main(request):
    title = 'uiRepublic'
    hot_products = random.sample(list(Product.objects.all()), 3)
    content = {
        'title': title,
        'hot_products': hot_products,
        # 'fact': Fact(),
    }
    return render(request, 'mainapp/index.html', content)


def catalog(request):
    title = 'Каталог'
    categories = ProductCategory.objects.all()
    
    content = {
        'title': title,
        'categories': categories,
    }
    return render(request, 'mainapp/catalog/catalog.html', content)


def category(request, category_pk, page=1):
    title = 'Категория'
    current_category = ProductCategory.objects.get(id=category_pk)
    products_category = Product.objects.filter(category__id=category_pk, is_active=True, category__is_active=True)

    paginator = Paginator(products_category, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': title,
        'current_category': current_category,
        'products_category': products_paginator,
    }
    return render(request, 'mainapp/catalog/category.html', content)


def product(request, category_pk, product_pk):
    category = ProductCategory.objects.get(id=category_pk)
    product = Product.objects.get(id=product_pk)
    title = product.name
    content = {
        'title': title,
        'category': category,
        'product': product,
        'specifications': str(product.specifications).split(';'),
    }
    return render(request, 'mainapp/catalog/product.html', content)


@cache_page(600)
def contact(request):
    title = 'Контакты'
    email = 'support@tech.com'
    content = {
        'title': title,
        'email': email
    }
    return render(request, 'mainapp/contact.html', content)
