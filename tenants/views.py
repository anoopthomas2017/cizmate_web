from django.shortcuts import render

def tenant_home(request):
    if request.tenant:
        tenant = request.tenant
        # Pass the tenant to the template
        return render(request, 'tenant_home.html', {'tenant': tenant})
    else:
        # If no tenant is found, handle the normal flow
        return render(request, 'home.html')
