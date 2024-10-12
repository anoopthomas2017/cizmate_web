from tenants.models import Tenant

class TenantRouter:
    def db_for_read(self, model, **hints):
        return self.get_tenant_database()

    def db_for_write(self, model, **hints):
        return self.get_tenant_database()

    def get_tenant_database(self):
        # Implement logic to determine the current tenant's database
        # This could be based on a request object, session, etc.
        # For example, using a subdomain or request header
        # Here we assume a function `get_current_tenant()` that returns the current tenant

        current_tenant = get_current_tenant()
        if current_tenant:
            return {
                'ENGINE': 'mssql',
                'NAME': current_tenant.db_name,
                # 'USER': current_tenant.db_user,
                # 'PASSWORD': current_tenant.db_password,
                # 'HOST': current_tenant.db_host,
                # 'PORT': current_tenant.db_port,
                'USER': 'sa',          # Your MSSQL username
                'PASSWORD': '123',      # Your MSSQL password
                'HOST': 'LAPTOP-8VRP7QRK\\SQLEXPRESS',  # Your host name
                'PORT': '1433', 
                'OPTIONS': {
                    'driver': 'SQL Server Native Client 11.0',
                },
            }
        return 'default'

def get_current_tenant(request=None):
    if request and hasattr(request, 'tenant'):
        return request.tenant
    return None