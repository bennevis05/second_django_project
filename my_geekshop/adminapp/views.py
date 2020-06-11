from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from adminapp.forms import ProductCategoryEditForm, ProductEditForm, ShopUserAdminEditForm
from authnapp.forms import ShopUserRegisterForm
from authnapp.models import ShopUser
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def admin_main(request):
    response = redirect("admin:users")
    return response


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    paginate_by = 2
    template_name = "adminapp/users.html"

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context["title"] = "админка | пользователи"
        return context


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = "пользователи | создание"

    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("admin:users"))
    else:
        user_form = ShopUserRegisterForm()

    content = {"title": title, "update_form": user_form, "media_url": settings.MEDIA_URL}

    return render(request, "adminapp/user_update.html", content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = "пользователи | редактирование"

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("admin:user_update", args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {"title": title, "update_form": edit_form, "media_url": settings.MEDIA_URL}

    return render(request, "adminapp/user_update.html", content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = "пользователи | удаление"

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        # user.delete()
        # Instead delete we will set users inactive
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse("admin:users"))

    content = {"title": title, "user_to_delete": user, "media_url": settings.MEDIA_URL}

    return render(request, "adminapp/user_delete.html", content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request, page=1):
    title = "админка | категории"
    categories_list = ProductCategory.objects.all()

    paginator = Paginator(categories_list, 2)
    try:
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        categories_paginator = paginator.page(1)
    except EmptyPage:
        categories_paginator = paginator.page(paginator.num_pages)

    content = {"title": title, "objects": categories_paginator, "media_url": settings.MEDIA_URL}
    return render(request, "adminapp/categories.html", content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = "категории/создание"

    if request.method == "POST":
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse("admin:categories"))
    else:
        category_form = ProductCategoryEditForm()

    content = {"title": title, "update_form": category_form, "media_url": settings.MEDIA_URL}

    return render(request, "adminapp/category_update.html", content)


class ProductCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("admin:categories")
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context["title"] = "категории | создание"
        return context


class ProductCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("admin:categories")
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context["title"] = "категории | редактирование"
        return context


class ProductCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = "adminapp/category_delete.html"
    success_url = reverse_lazy("admin:categories")

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryDeleteView, self).get_context_data(**kwargs)
        context["title"] = "категории | удаление"
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk, page=1):
    title = "админка | продукты"
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by("name")

    paginator = Paginator(products_list, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        "title": title,
        "category": category,
        "objects": products_paginator,
        "media_url": settings.MEDIA_URL
    }
    return render(request, "adminapp/products.html", content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт | создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {'title': title, 
               'update_form': product_form, 
               'category': category
    }

    return render(request, 'adminapp/product_update.html', content)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "adminapp/product_read.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["title"] = "продукт | подробно"
        return context


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт | редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)
    
    content = {'title': title, 
               'update_form': edit_form, 
               'category': edit_product.category 
    }
    
    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт | удаление'

    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))

    content = {'title': title, 'product_to_delete': product}
    
    return render(request, 'adminapp/product_delete.html', content)
