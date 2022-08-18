from django.db import models

# Create your models here.

class user_detail(models.Model):
    sid = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=120)
    dob = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=120)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    aadhar = models.CharField(max_length=12)
    gender = models.CharField(max_length=10)
    active_status = models.CharField(max_length=20)
    community = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class institution_detail(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)
    type_insti = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    contact = models.CharField(max_length=14, null=True, blank=True)

class degree(models.Model):
    sid =  models.ForeignKey(user_detail, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    insti_id = models.ForeignKey(institution_detail, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    discipline = models.CharField(max_length=20)
    date_join = models.DateField()
    date_leave = models.DateField()
    grade = models.CharField(max_length=10)

class course(models.Model):
    degree_id=models.ForeignKey(degree, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total_marks = models.CharField(max_length=10)
    obtained_marks = models.CharField(max_length=10)
    credits = models.CharField(max_length=10)
    semester = models.CharField(max_length=2)

