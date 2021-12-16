from django.db import models


class Item(models.Model):
    class Meta:
        db_table = 'items'
    name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255)
    current_date = models.DateTimeField()
    current_price = models.FloatField()
    link = models.CharField(max_length=255)

    def list(self):
        return Item.objects.all()


class Category(models.Model):
    class Meta:
        db_table = 'categories'

    category_name = models.CharField(max_length=254)

    def list(self):
        return Category.objects.all()
