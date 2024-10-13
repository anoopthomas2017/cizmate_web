from tenants.models import Tenant
from django.contrib.sites.shortcuts import get_current_site

class TenantRouter:
    def db_for_read(self, model, **hints):
        """Route read operations to the correct tenant database."""
        return self.get_tenant_database(hints)

    def db_for_write(self, model, **hints):
        """Route write operations to the correct tenant database."""
        return self.get_tenant_database(hints)

    def get_tenant_database(self, hints):
        """Determine and return the current tenant's database configuration."""
        current_tenant = hints.get('tenant') or get_current_tenant()  # Get tenant from hints or global method
        
        if current_tenant:  
            # Log the current tenant for debugging
            print(f'Current tenant: {current_tenant.name}')
            
            # Return tenant-specific MSSQL database configuration
            return {
                'ENGINE': 'mssql',
                'NAME': current_tenant.db_name,  # Database name from tenant
                'USER': 'sa',                   # MSSQL username (adjust if needed)
                'PASSWORD': '123',               # MSSQL password (adjust if needed)
                'HOST': 'LAPTOP-8VRP7QRK\\SQLEXPRESS',  # Hostname
                'PORT': '1433',                  # MSSQL default port
                'OPTIONS': {
                    'driver': 'SQL Server Native Client 11.0',  # MSSQL driver
                },
            }
        
        # Default to the main database if no tenant is found
        ##return 'default'
def get_current_tenant(request=None):
    """Determine the current tenant based on the subdomain."""
    if not request:
        return None

    # Get the current site (e.g., 'example.com')
    current_site = get_current_site(request)
    
    # Extract subdomain from the domain (e.g., 'subdomain.example.com')
    domain_parts = current_site.domain.split('.')
    if len(domain_parts) > 1:
        subdomain = domain_parts[0]  # Subdomain is typically the first part of the domain
    else:
        # No subdomain found, return None or handle as needed
        return None

    # Try to get the tenant based on the subdomain
    try:
        return Tenant.objects.get(name=subdomain)
    except Tenant.DoesNotExist:
        # Handle the case where the tenant is not found
        return None
