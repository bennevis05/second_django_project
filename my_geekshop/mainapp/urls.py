from django.urls import re_path

import mainapp.views as mainapp

app_name = "mainapp"

urlpatterns = [
    re_path(r"^$", mainapp.catalog, name="main"),
    re_path(r"^(?P<category_pk>\d+)/$", mainapp.category, name="category"),
    re_path(r"^(?P<category_pk>\d+)/page/(?P<page>\d+)/$", mainapp.category, name="page"),
    re_path(r"^(?P<category_pk>\d+)/(?P<product_pk>\d+)/$", mainapp.product, name="product"),
]
