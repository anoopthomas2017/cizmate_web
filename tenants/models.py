import re
from django.core.exceptions import ValidationError


# Create your models here.
from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    db_name = models.CharField(max_length=100)
    db_user = models.CharField(max_length=100)
    db_password = models.CharField(max_length=100)
    db_host = models.CharField(max_length=100)
    db_port = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
def validate_gst_number(value):
    # Regex for validating GST number
    # gst_pattern = r'^[0-9]{2}[A-Z]{4}[0-9]{4}[A-Z]{1}[0-9]{1}[Z]{1}[0-9A-Z]{1}$'
    gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    if not re.match(gst_pattern, value):
        raise ValidationError(f"{value} is not a valid GST number.")

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255, blank=False)
    sub_head1 = models.CharField(max_length=255, blank=True, null=True)
    sub_head2 = models.CharField(max_length=255, blank=True, null=True)
    sub_head3 = models.CharField(max_length=255, blank=True, null=True)
    c_phone = models.CharField(max_length=20, blank=True, null=True)
    c_fax = models.CharField(max_length=20, blank=True, null=True)
    c_mail = models.EmailField(blank=True, null=True)
    c_mobile = models.CharField(max_length=20, blank=True, null=True)
    cst = models.CharField(max_length=20, blank=True, null=True)
    tin_no = models.CharField(max_length=20, blank=True, null=True)
    
    # GSTIN field with validation
    gstin = models.CharField(
        max_length=15,
        validators=[validate_gst_number],
        blank=True,
        null=True
    )
    
    pan = models.CharField(max_length=20, blank=True, null=True)
    bank = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Terms(models.Model):
    company_info = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE, related_name='terms')
    term1 = models.TextField(blank=True, null=True)
    term2 = models.TextField(blank=True, null=True)
    term3 = models.TextField(blank=True, null=True)
    term4 = models.TextField(blank=True, null=True)
    term5 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Terms for {self.company_info.name}'
    