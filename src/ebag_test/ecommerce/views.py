from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse

import json

from .models import *
from .forms import *

def categories(request):
    sub_categories = Category.objects.filter(parent=None)
    return render(request, 'ecommerce/categories.html', {'sub_categories': sub_categories})

def get_parent_categories(category):
    if category.parent:
        return get_parent_categories(category.parent) + [category.parent]
    return []

def category(request, id):
    category = get_object_or_404(Category, id=id)
    parent_categories = get_parent_categories(category)
    sub_categories = Category.objects.filter(parent=category)
    products = Product.objects.filter(category=category)
    return render(request, 'ecommerce/category.html', {
        'category': category,
        'parent_categories': parent_categories,
        'sub_categories': sub_categories,
        'products': products
    })

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    return render(request, 'ecommerce/category_form.html', { 'form': form })

def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    return render(request, 'ecommerce/category_form.html', { 'form': form })

def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'ecommerce/category_delete.html', { 'category': category })

def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'ecommerce/product.html', { 'product': product })

def product_create(request, category_id):
    if request.method == 'POST':
        form = ProductForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('category', kwargs={ 'id': form.instance.category_id }))
    form = ProductForm(initial={'category': category_id})
    return render(request, 'ecommerce/product_form.html', {
        'form': form,
        'category_id': category_id
    })

def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('category', kwargs={ 'id': form.instance.category_id }))
    form = ProductForm(instance=product)
    return render(request, 'ecommerce/product_form.html', {
        'form': form,
        'category_id': product.category.id
    })

def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        url = reverse('category', kwargs={ 'id': product.category.id })
        product.delete()
        return redirect(url)
    return render(request, 'ecommerce/product_delete.html', { 'product': product })

# Examples:
# http://localhost:8000/search/?title=%D0%9F%D0%B8%D0%BB
# http://localhost:8000/search/?has_image=false
def search(request):
    filters = []
    excludes = []

    if request.GET.get('title', '').strip():
        title = request.GET['title'].strip()
        filters.append(Q(title__icontains=title) | Q(description__icontains=title))

    if request.GET.get('sku', '').strip():
        filters.append(Q(sku__icontains=request.GET['sku'].strip()))

    if request.GET.get('category', '').strip():
        filters.append(Q(category__name__icontains=request.GET['category'].strip()))

    if request.GET.get('from_price', '').strip():
        filters.append(Q(price__gte=request.GET['from_price'].strip()))

    if request.GET.get('to_price', '').strip():
        filters.append(Q(price__lte=request.GET['to_price'].strip()))

    if request.GET.get('has_image', '').strip():
        has_image = request.GET['has_image'].strip().lower() == 'true'
        if has_image:
            excludes.append(Q(image=''))
        else:
            filters.append(Q(image=''))

    products = Product.objects.filter(*filters).exclude(*excludes)
    return render(request, 'ecommerce/products.html', { 'products': products })

# Examples:
# http://localhost:8000/search_api/?params={%22title%22:%20%22%D0%B4%D0%BE%D0%BC%D0%B0%D1%82%22,%20%22has_image%22:%20true}
def search_api(request) -> list[Product]:
    request_params = request.GET.get('params', '').strip()
    filters = []
    excludes = []

    if request_params:
        params: SearchRequest = json.loads(request_params)

        if params.get('title') and params['title'].strip():
            title = params['title'].strip()
            filters.append(Q(title__icontains=title) | Q(description__icontains=title))

        if params.get('sku') and params['sku'].strip():
            filters.append(Q(sku__icontains=params['sku'].strip()))

        if params.get('category') and params['category'].strip():
            filters.append(Q(category__name__icontains=params['category'].strip()))

        if params.get('from_price') and params['from_price']:
            filters.append(Q(price__gte=params['from_price']))

        if params.get('to_price') and params['to_price']:
            filters.append(Q(price__lte=params['to_price']))

        if params.get('has_image'):
            if params['has_image']:
                excludes.append(Q(image=''))
            else:
                filters.append(Q(image=''))

    products = Product.objects.filter(*filters).exclude(*excludes).values()
    return JsonResponse(list(products), safe=False)
