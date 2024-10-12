# Generated by Django 5.0.9 on 2024-10-12 12:05

import django.db.models.deletion
import tenants.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sub_head1', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_head2', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_head3', models.CharField(blank=True, max_length=255, null=True)),
                ('c_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('c_fax', models.CharField(blank=True, max_length=20, null=True)),
                ('c_mail', models.EmailField(blank=True, max_length=254, null=True)),
                ('c_mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('cst', models.CharField(blank=True, max_length=20, null=True)),
                ('tin_no', models.CharField(blank=True, max_length=20, null=True)),
                ('gstin', models.CharField(blank=True, max_length=15, null=True, validators=[tenants.models.validate_gst_number])),
                ('pan', models.CharField(blank=True, max_length=20, null=True)),
                ('bank', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term1', models.TextField(blank=True, null=True)),
                ('term2', models.TextField(blank=True, null=True)),
                ('term3', models.TextField(blank=True, null=True)),
                ('term4', models.TextField(blank=True, null=True)),
                ('term5', models.TextField(blank=True, null=True)),
                ('company_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='tenants.companyinfo')),
            ],
        ),
    ]
