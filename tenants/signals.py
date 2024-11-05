from django.db import connections
from django.db.models.signals import post_save, pre_init
from django.dispatch import receiver
from django.conf import settings
from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from .models import Tenant
import pyodbc

def get_tenant_db_config(tenant_name):
    try:
        
        tenant = Tenant.objects.using('default').get(name=tenant_name)
        return {
            'NAME': tenant.db_name,
            'USER': tenant.db_user,
            'PASSWORD': tenant.db_password,
            'HOST': tenant.db_host,
            'PORT': tenant.db_port,
        }
    except Tenant.DoesNotExist:
        return None

def check_and_apply_migrations(tenant_name):
    print('check_and_apply_migrations')
   
    tenant_data=tenant_name.name
   
    db_config = get_tenant_db_config(tenant_data)
    if not db_config:
        print(f"Tenant {tenant_data} not found")
        return
    
    try:
        connection = connections[tenant_data]
        executor = MigrationExecutor(connection)
        if executor.migration_plan(executor.loader.graph.leaf_nodes()):
            print(f"Applying migrations for tenant: {tenant_data}")
            call_command('migrate', database=tenant_data)
        else:
            print(f"No pending migrations for tenant: {tenant_data}")
    except Exception as e:
        print(f"Migration check failed for {tenant_data}: {str(e)}")

@receiver(pre_init)
def ensure_tenant_migrations(sender, **kwargs):
    try:
        if hasattr(kwargs.get('instance', None), '_state'):
            tenant_name = kwargs['instance']
            if tenant_name and tenant_name != 'default':
                check_and_apply_migrations(tenant_name)
    except Exception as e:
        print(f"Migration signal failed: {str(e)}")

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