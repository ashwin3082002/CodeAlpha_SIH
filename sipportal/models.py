from django.db import models




# Create your models here.

class user_details(models.Model):
    sid = models.CharField(primary_key=True)
    name = models.CharField()
    dob = models.DecimalField(max_digits=4, decimal_places=0)
    guardian_name = models.CharField()
    email = models.EmailField()
    mobile = models.DecimalField(max_digits=10, decimal_places=None)
    aadhar = models.DecimalField(max_digits=12, deciaml_places=None)
    gender = models.CharField()
    active_status = models.CharField()
    community = models.CharField()

    def __str__(self):
        return self.name
