from django.db import models

# Create your models here.

class user_details(models.Model):
    sid = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=120)
    dob = models.DecimalField(max_digits=4, decimal_places=0)
    guardian_name = models.CharField(max_length=120)
    email = models.EmailField()
    mobile = models.DecimalField(max_digits=10, decimal_places=0)
    aadhar = models.DecimalField(max_digits=12, decimal_places=0)
    gender = models.CharField(max_length=10)
    active_status = models.CharField(max_length=20)
    community = models.CharField(max_length=10)

    def __str__(self):
        return self.name
