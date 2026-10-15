"""
URL configuration for ebag_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .ecommerce import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.categories, name='categories'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:id>/', views.category, name='category'),
    path('categories/<int:id>/update/', views.category_update, name='category_update'),
    path('categories/<int:id>/delete/', views.category_delete, name='category_delete'),

    path('products/<int:category_id>/create/', views.product_create, name='product_create'),
    path('products/<int:id>/', views.product, name='product'),
    path('products/<int:id>/update/', views.product_update, name='product_update'),
    path('products/<int:id>/delete/', views.product_delete, name='product_delete'),

    path('search/', views.search, name='search'),
    path('search_api/', views.search_api, name='search_api'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
