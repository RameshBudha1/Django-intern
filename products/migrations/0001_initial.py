# Generated by Django 4.1.3 on 2023-08-22 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cateogry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cateogry_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.FloatField()),
                ('product_image', models.CharField(max_length=200)),
                ('product_quantity', models.IntegerField()),
                ('product_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cateogry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.cateogry')),
            ],
        ),
    ]