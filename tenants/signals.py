from django.db import connections
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.management import call_command
from .models import Tenant
import pyodbc

@receiver(post_save, sender=Tenant)
def create_tenant_database(sender, instance, created, **kwargs):
    if created:
        # Create a separate connection for database creation
        conn_str = (
            f"DRIVER={{SQL Server Native Client 11.0}};"
            f"SERVER={instance.db_host};"
            f"DATABASE=master;"
            f"UID={instance.db_user};"
            f"PWD={instance.db_password};"
        )
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {instance.db_name}")

        # Configure the new database settings
        tenant_db_config = {
            'ENGINE': 'mssql',
            'NAME': instance.db_name,
            'USER': instance.db_user,
            'PASSWORD': instance.db_password,
            'HOST': instance.db_host,
            'PORT': instance.db_port,
            'OPTIONS': {
                'driver': 'SQL Server Native Client 11.0',
            },
            'TIME_ZONE':'UTC',
            'CONN_HEALTH_CHECKS': False,
            'CONN_MAX_AGE': 0,
            'AUTOCOMMIT': True,
            'ATOMIC_REQUESTS': False,
            'TEST': {'CHARSET': None,
                      'COLLATION': None,
                      'MIGRATE': True,
                      'MIRROR': None,
                      'NAME': None},
        }
        settings.DATABASES['tenant'] = tenant_db_config

        # Run migrations for the tenant database
        call_command('migrate', database='tenant')

        # Clean up the temporary database configuration
        del settings.DATABASES['tenant']