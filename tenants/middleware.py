from tenants.models import Tenant
from django.http import HttpResponseNotFound
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This will be executed for each request before the view is called
        host = request.get_host().split('.')
        logger.debug(f"Host split: {host}")

        # Check if there is a subdomain (i.e., more than two segments in the domain)
        subdomain = host[0] #if len(host) > 2 else None
        logger.debug(f"Subdomain extracted: {subdomain}")

        if subdomain:
            try:
                request.tenant = Tenant.objects.get(name=subdomain)
                logger.debug(f"Tenant found: {request.tenant.name}")
                self.run_migrations_if_needed(request.tenant)
            except Tenant.DoesNotExist:
                logger.error(f"Invalid subdomain: '{subdomain}' does not match any tenant.")
                # Return 404 if the subdomain does not match any tenant
                return HttpResponseNotFound(f"Tenant '{subdomain}' not found")
        else:
            # No subdomain, proceed normally without assigning a tenant
            request.tenant = None
            logger.debug("No subdomain detected, proceeding without tenant assignment.")

        # Call the next middleware or the view
        return self.get_response(request)
    def run_migrations_if_needed(self, tenant):
        # Check for unapplied migrations (this step might vary based on your setup)
        try:
            logger.info(f"Checking for migrations for tenant: {tenant.name}")
            
            # Run the migrate command for the tenant's database
            call_command('migrate', database=tenant.db_name, interactive=False)
            
            logger.info(f"Migrations applied for tenant: {tenant.name}")
        except Exception as e:
            logger.error(f"Error applying migrations for tenant {tenant.name}: {e}")