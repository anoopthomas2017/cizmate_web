from cizmate_web.db_router import get_current_tenant
from tenants.models import Tenant
from django.http import HttpResponseNotFound
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware:
   def __init__(self, get_response):
        self.get_response = get_response

   def __call__(self, request):
        # Set the tenant for the request
        request.tenant = get_current_tenant(request)
        
        if request.tenant:
            print(f'Tenant set for request: {request.tenant}')
        else:
             print('No tenant found for request.')

        return self.get_response(request)
