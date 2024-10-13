from django.db import connections
from threading import local

_thread_local = local()

class DynamicTenantDatabaseRouter:
    def _get_tenant_db_name(self):
        return getattr(_thread_local, 'tenant_db_name', 'default')

    def db_for_read(self, model, **hints):
        return self._get_tenant_db_name()

    def db_for_write(self, model, **hints):
        return self._get_tenant_db_name()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

    @staticmethod
    def set_tenant_db_name(tenant_db_name):
        _thread_local.tenant_db_name = tenant_db_name

    @staticmethod
    def setup_tenant_db(tenant):
        if tenant.name not in connections.databases:
            connections.databases[tenant.name] = {
                'ENGINE': 'mssql',
                'NAME': tenant.db_name,  # Database name from tenant
                'USER': 'sa',                   # MSSQL username (adjust if needed)
                'PASSWORD': '123',               # MSSQL password (adjust if needed)
                'HOST': 'LAPTOP-8VRP7QRK\\SQLEXPRESS',  # Hostname
                'PORT': '1433',                  # MSSQL default port
                'OPTIONS': {
                    'driver': 'SQL Server Native Client 11.0',  # MSSQL driver
                },
                'ATOMIC_REQUESTS': False,  # Add this line
                'AUTOCOMMIT': True,        # Add this line
                'CONN_MAX_AGE': 0,         # Add this line
                'TIME_ZONE': None,         # Add this line
                'CONN_HEALTH_CHECKS': False, # Add this line
                'TEST': {                  # Add this block
                    'NAME': None,
                    'CHARSET': None,
                    'COLLATION': None,
                    'MIRROR': None,
                },
            }