# Generated by Django 3.2.9 on 2021-12-14 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('item_type', models.CharField(max_length=255)),
                ('current_date', models.DateTimeField()),
                ('current_price', models.FloatField()),
                ('link', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'items',
            },
        ),
    ]
