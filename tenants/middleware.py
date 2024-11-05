from django.apps import apps

from cizmate_web.db_router import DynamicTenantDatabaseRouter


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host_parts = request.get_host().split('.')
        # print('--------host_parts--------')
        # print(host_parts)
        # print('----------------')
        subdomain = host_parts[0] if len(host_parts) > 1 else None
        # print('--------subdomain--------')
        # print(subdomain)
        # print('----------------')
        Tenant = apps.get_model('tenants', 'Tenant')
     
        tenant = None
        if subdomain:
            tenant = Tenant.objects.using('default').filter(name=subdomain).first()
           
        if tenant:
            request.tenant = tenant
            DynamicTenantDatabaseRouter.setup_tenant_db(tenant)
            DynamicTenantDatabaseRouter.set_tenant_db_name(tenant.name)
        else:
            request.tenant = None
            DynamicTenantDatabaseRouter.set_tenant_db_name('default')
        
        response = self.get_response(request)
        return response