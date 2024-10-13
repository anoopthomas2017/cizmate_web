from django.shortcuts import render

from tenants.models import CompanyInfo
def tenant_home(request):
    
    
    if request.tenant:
        tenant = request.tenant
        tenant_data = CompanyInfo.objects.all()
        # Pass the tenant to the template
        context = {
            'tenant': tenant,
            'company': tenant_data
        }
        return render(request, 'tenant_home.html', context)
    else:
        # If no tenant is found, handle the normal flow
        return render(request, 'home.html')
