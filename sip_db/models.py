from django.db import models

# Create your models here.

class user_details(models.Model):
    sid = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=120)
    dob = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=120)
    email = models.EmailField()
    mobile = models.DecimalField(max_digits=10, decimal_places=0)
    aadhar = models.CharField(max_length=12)
    gender = models.CharField(max_length=10)
    active_status = models.CharField(max_length=20)
    community = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class institution_details():
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    type_insti = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    contact = models.CharField(max_length=14)

class degree(models.Model):
    sid =  models.ForeignKey(user_details)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    insti_id = models.ForeignKey(institution_details)
    status = models.CharField(max_length=10)
    discipline = models.CharField(max_length=20)
    date_join = models.DateField()
    date_leave = models.DateField()
    grade = models.CharField(max_length=10)



