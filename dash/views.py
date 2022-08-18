import email
from email.headerregistry import Address
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from sip_db.models import institution_detail, student_detail
from util import func

# Create your views here.
def admin(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            i_name = request.POST.get('ins-name')
            i_type = request.POST.get('type')
            i_email = request.POST.get('email')
            i_contact = request.POST.get('contact')
            i_state = request.POST.get('state')
            i_city = request.POST.get('city')
            i_pincode = request.POST.get('pincode')

            # must add contact later
            #database instance
            db_insti = institution_detail(
                id= func.insti_id_gen(),
                name=i_name,
                type_insti=i_type,
                email=i_email,
                contact = i_contact,
                state = i_state,
                city = i_city,
                pincode = i_pincode,
            )
            db_insti.save()
            # db_insti.name = i_name
            # db_insti.type_insti = i_type
            # db_insti.email = i_email
            # db_insti.contact = i_contact
            # db_insti.state = i_state
            # db_insti.city = i_city
            # db_insti.pincode = i_pincode
            # db_insti.save()
            print('Database Updated :)')

            return redirect('/dashboard/admin')
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        return render(request, 'dashboards\dashboard_admin.html',{'username':uname, 'name':nam, 'email':user_email})
    else:
        return redirect('/login/admin')


def student(request):
    if request.user.is_authenticated:
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        return render(request, 'dashboards\dashboard_student.html',{'username':uname, 'name':nam, 'email':user_email})
    else:
        return redirect('/login/student')

def institution(request):
    if request.user.is_authenticated:
        if request.method == "POST":
                s_name = request.POST.get('stu-name')
                dob = request.POST.get('dob')
                guardian = request.POST.get('guardian')
                aadhar = request.POST.get('aadhar')
                gender = request.POST.get('gender')
                email = request.POST.get('email')
                contact = request.POST.get('contact')
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                pincode = request.POST.get('pincode')
                community = request.POST.get('community')

                db_student = student_detail(
                    sid = func.stu_id_gen(),
                    name = s_name,
                    dob= dob,
                    guardian_name = guardian,
                    email= email,
                    mobile=contact,
                    aadhar=aadhar,
                    gender=gender,
                    active_status=False,
                    community= community,
                    #new
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode
                )

                db_student.save()
                print('Database Updated :)')


        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        return render(request, 'dashboards\dashboard_institution.html',{'username':uname, 'name':nam, 'email':user_email})
    else:
        return redirect('/login/institution')