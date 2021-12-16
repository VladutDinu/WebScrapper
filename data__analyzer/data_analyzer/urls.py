"""data_analyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from dataAnalyzer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', views.ItemView.as_view(),),
    path('categories/', views.CategoryView.as_view(),),
    path('items_page/<category>', views.item_page),
    path('item_history/<name>', views.item_history),
    path('scrapper/', views.scrapper),
    path('scrapper/scrap_method/', views.scrap_method),
    path('categories_page/', views.categories_page),
    path('category_operations/', views.category_operations),
    path('add_category', views.add_category),
    path('delete_category/', views.delete_category),
    path('update_category/', views.update_category),
    path('', views.homepage)
]
