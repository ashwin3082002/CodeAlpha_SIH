from django.db import models

# Create your models here.

class student_detail(models.Model):
    sid = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=120)
    dob = models.CharField(max_length=20)
    guardian_name = models.CharField(max_length=120)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    aadhar = models.CharField(max_length=12)
    gender = models.CharField(max_length=10)
    active_status = models.CharField(max_length=20)
    community = models.CharField(max_length=10)
    address = models.TextField(default='')
    city = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=20, default='')
    pincode = models.CharField(max_length=6, default='')
    profile_pic = models.ImageField(null = True, blank = True , upload_to = 'profilepic/student')
    
    
    
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
    profile_pic = models.ImageField(null = True, blank = True , upload_to = 'profilepic/institutuion/')

    def __str__(self):
        return self.name

class degree(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(student_detail, on_delete=models.CASCADE, db_column='sid')
    iid = models.ForeignKey(institution_detail, on_delete=models.CASCADE, db_column='iid')
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10) # Pursuing, Drop , Completed
    discipline = models.CharField(max_length=20)
    year_join = models.CharField(max_length=10)
    year_leave = models.CharField(max_length=10, blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class course(models.Model):
    cid=models.AutoField(primary_key=True)
    did= models.ForeignKey(degree, on_delete=models.CASCADE, db_column='did')
    name = models.CharField(max_length=100)
    total_marks = models.CharField(max_length=10)
    obtained_marks = models.CharField(max_length=10)
    credits = models.CharField(max_length=10)
    semester = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class docreq(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(student_detail, on_delete=models.CASCADE, db_column='sid')
    i_id = models.ForeignKey(institution_detail, on_delete=models.CASCADE, db_column='i_id')
    doc_type = models.CharField(max_length=20)
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id}'

class api_details(models.Model):
    api_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    api_key = models.CharField(max_length=200)
    permissions = models.CharField(max_length=100)

    def __str__(self):
        return self.org_name

class account_detail(models.Model):
    acc_id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(student_detail, on_delete=models.CASCADE)
    holder_name = models.CharField(max_length=50)
    acc_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=100)
    ifsc = models.CharField(max_length=50)
    def __str__(self):
        return str(self.acc_id)

class institution_id(models.Model):
    instiid= models.CharField(max_length=50)
    def __str__(self):
        return self.instiid

class student_id(models.Model):
    stuid= models.CharField(max_length=50)
    def __str__(self):
        return self.stuid
