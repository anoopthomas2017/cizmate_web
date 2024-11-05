from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from django.shortcuts import get_object_or_404

from tenants.signals import check_and_apply_migrations
from .models import CompanyInfo, Terms
from .serializers import CompanyInfoSerializer, TermsSerializer

def tenant_home(request):
    print (request.tenant)
    print (request.tenant)
    tenant_data = CompanyInfo.objects.all()
    print(tenant_data)
    if request.tenant:

        tenant = request.tenant
        tenant_data = CompanyInfo.objects.all()
        check_and_apply_migrations(request.tenant)
        # Pass the tenant to the template
        context = {
            'tenant': tenant,
            'company': tenant_data
        }
        return render(request, 'tenant_home.html', context)
    else:
        # If no tenant is found, handle the normal flow
        return render(request, 'home.html')
class CompanyInfoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling single CompanyInfo instance
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def list(self, request):
        """Get company details"""
        company = CompanyInfo.objects.first()
        if company:
            serializer = CompanyInfoSerializer(company)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        return Response({
            'status': 'success',
            'data': None,
            'message': 'No company information exists'
        })

    def retrieve(self, request, pk=None):
        """Get company details by ID"""
        company = CompanyInfo.objects.first()
        if company and str(company.pk) == str(pk):
            serializer = CompanyInfoSerializer(company)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Company not found'
        }, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Create new company if none exists"""
        if CompanyInfo.objects.exists():
            return Response({
                'status': 'error',
                'message': 'Company information already exists. Use update instead.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CompanyInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Company created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update existing company"""
        company = CompanyInfo.objects.first()
        if not company or (pk and str(company.pk) != str(pk)):
            return Response({
                'status': 'error',
                'message': 'Company not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanyInfoSerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Company updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete the company"""
        company = CompanyInfo.objects.first()
        if not company or (pk and str(company.pk) != str(pk)):
            return Response({
                'status': 'error',
                'message': 'Company not found'
            }, status=status.HTTP_404_NOT_FOUND)

        company.delete()
        return Response({
            'status': 'success',
            'message': 'Company deleted successfully'
        }, status=status.HTTP_200_OK)

class TermsViewSet(viewsets.ViewSet):
    """
    ViewSet for handling Terms CRUD operations via API
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def list(self, request):
        terms = Terms.objects.all()
        serializer = TermsSerializer(terms, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def retrieve(self, request, pk=None):
        terms = get_object_or_404(Terms, pk=pk)
        serializer = TermsSerializer(terms)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def create(self, request):
        serializer = TermsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Terms created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        terms = get_object_or_404(Terms, pk=pk)
        serializer = TermsSerializer(terms, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Terms updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        terms = get_object_or_404(Terms, pk=pk)
        terms.delete()
        return Response({
            'status': 'success',
            'message': 'Terms deleted successfully'
        }, status=status.HTTP_200_OK)