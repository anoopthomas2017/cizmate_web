# Generated by Django 5.0.9 on 2024-11-04 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Unique code for the category', max_length=20, unique=True, verbose_name='Category Code')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(editable=False, max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='inventory.category', verbose_name='Parent Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['code'], name='inventory_c_code_710414_idx'), models.Index(fields=['name'], name='inventory_c_name_546ce4_idx'), models.Index(fields=['slug'], name='inventory_c_slug_9e1826_idx')],
            },
        ),
    ]
