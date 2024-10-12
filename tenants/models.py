from django.db import models

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