from rest_framework.response import Response
from django.shortcuts import render
from dataAnalyzer import serializers
from dataAnalyzer.serializers import ItemSerializer, CategorySerializer
from rest_framework.views import APIView
from dataAnalyzer.scripts.scrapper import Scrapper
from dataAnalyzer.models import Item, Category
import collections
# Create your views here.


class ItemView(APIView):
    def __init__(self):
        self.items = Item.objects.all()
        self.serializer = ItemSerializer

    def get(self, *args, **kwargs):
        return Response(self.serializer(self.items, many=True).data)


def get_unique_items_of_category(category):
    itemV = ItemView()
    items = itemV.items.filter(item_type=category)
    seen = collections.OrderedDict()
    for obj in items:
        # eliminate this check if you want the last item
        if obj.name not in seen:
            seen[obj.name] = obj

    final_values = list(seen.values())
    return items, final_values, itemV


def scrap(category):
    scrapper_obj = Scrapper()
    try:
        scrapper_obj.run(str(category))
    except:
        raise ValueError("Categoria nu exista pe site-ul Emag")


def item_page(request, category):
    items, final_values, itemV = get_unique_items_of_category(category)
    if len(items) > 1:
        return render(request, 'items.html', {
            "items": itemV.serializer(final_values, many=True).data
        })
    else:
        print("Scrapping")
        try:
            scrap(category)
            items, final_values, itemV = get_unique_items_of_category(category)
            return render(request, 'items.html', {
                "items": itemV.serializer(final_values, many=True).data
            })
        except:
            return render(request, "category_not_found.html")


def scrapper(request):
    categoriesV = CategoryView()
    return render(request, 'scrapper.html', {
        "categories": categoriesV.serializer(categoriesV.categories, many=True).data
    })


def homepage(request):
    return render(request, 'base.html')


class CategoryView(APIView):
    def __init__(self):
        self.categories = Category.objects.all()
        self.serializer = CategorySerializer

    def get(self, *args, **kwargs):
        return Response(self.serializer(self.categories, many=True).data)


def categories_page(request):
    categoriesV = CategoryView()
    return render(request, 'categories.html', {
        "categories": categoriesV.serializer(categoriesV.categories, many=True).data
    })


def scrap_method(request):
    category = request.GET.get("category")
    scrap(category)
    print("Scrapping")
    return item_page(request, category)


def item_history(request, name):
    itemV = ItemView()
    items = itemV.items.filter(name=name)
    min_item = itemV.items.filter(name=name).order_by('current_price')
    if len(items) != 0:
        return render(request, 'item_history.html', {
            "items": itemV.serializer(items, many=True).data,
            "minmax": [itemV.serializer(min_item, many=True).data[0], itemV.serializer(min_item, many=True).data[-1]]
        })
    else:
        return item_page(request, items[0].item_type)


def category_operations(request):
    categoriesV = CategoryView()
    return render(request, 'category_operations.html', {
        "categories": categoriesV.serializer(categoriesV.categories, many=True).data
    })


def add_category(request):
    category = request.GET.get("category")
    if len(category) > 1:
        cat = Category(category_name=category).save()

        categoriesV = CategoryView()
        return render(request, 'categories.html', {
            "categories": categoriesV.serializer(categoriesV.categories, many=True).data
        })
    else:
        return render(request, "add_404.html")


def delete_category(request):
    try:
        category_id = request.GET.get('category_id')
        cat = Category(id=category_id).delete()
        categoriesV = CategoryView()
        return render(request, 'category_operations.html', {
            "categories": categoriesV.serializer(categoriesV.categories, many=True).data
        })
    except:
        categoriesV = CategoryView()
        return render(request, 'category_operations.html', {
            "categories": categoriesV.serializer(categoriesV.categories, many=True).data
        })


def update_category(request):
    try:
        category_id = request.GET.get('category_id')
        category_new_name = request.GET.get('category_new_name')
        cat = Category(id=category_id)
        cat.category_name = category_new_name
        cat.save()
        categoriesV = CategoryView()
        return render(request, 'category_operations.html', {
            "categories": categoriesV.serializer(categoriesV.categories, many=True).data
        })
    except:
        categoriesV = CategoryView()
        return render(request, 'category_operations.html', {
            "categories": categoriesV.serializer(categoriesV.categories, many=True).data
        })
