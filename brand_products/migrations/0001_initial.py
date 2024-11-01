# Generated by Django 5.1.2 on 2024-10-21 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('asin', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=255, null=True)),
                ('image_url', models.CharField(max_length=1024)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='brand_products.brand')),
            ],
        ),
    ]
