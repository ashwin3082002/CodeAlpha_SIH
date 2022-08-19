import email
from email import message
from email.headerregistry import Address
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from sip_db.models import institution_detail, student_detail, degree, course
from util import func
from django.contrib import messages

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

            #generate insti id
            i_id = func.insti_id_gen()

            # must add contact later
            #database instance
            db_insti = institution_detail(
                id= i_id,
                name=i_name,
                type_insti=i_type,
                email=i_email,
                contact = i_contact,
                state = i_state,
                city = i_city,
                pincode = i_pincode,
            )
            db_insti.save()

            #create new user and grant staff status
            User.objects.create_user(
                username = i_id, 
                email = i_email,
                password = 'password',
                is_staff = True
            )
            #new_user.is_staff = True
            print('id: ', i_id)
            print('Database Updated :)')

            messages.success(request, "Successfully created institution profile.")

            # to send id and pass as email

            return redirect('/dashboard/admin')

        # getting username from login
        uname=request.user.get_username()
        # getting other user details in a obj 'user'
        user = User.objects.get(username=uname)

        user_email = user.email
        name = user.get_full_name()
        return render(request, 'dashboards\dashboard_admin.html',{'username':uname, 'name':name, 'email':user_email})
    else:
        return redirect('/login/admin')

def admin_search(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if 'search' in request.POST:
                i_id = request.POST.get('institution-id')
                search_details = institution_detail.objects.filter(id = i_id).values()
                if search_details:
                    return render(request, 'dashboards\dashboard_admin_search.html', {'i': search_details[0]})
                else:
                    messages.error(request, "Institution not found.")
                    return render(request, 'dashboards\dashboard_admin_search.html')
        else:
            return render(request, 'dashboards\dashboard_admin_search.html')
    else:
        return redirect('/login/admin')
    
def admin_edit(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            # search insti
            if 'search' in request.POST:
                i_id = request.POST.get('institution-id')
                search_details = institution_detail.objects.filter(id = i_id).values()
                if search_details:
                    return render(request, 'dashboards\dashboard_admin_edit.html', {'i': search_details[0]})
                else:
                    messages.error(request, "Institution not found.")
                    return render(request, 'dashboards\dashboard_admin_edit.html')


            # change insti details
            if 'edit' in request.POST:
                i_id = request.POST.get('institution-id')
                i_name = request.POST.get('ins-name')
                i_type = request.POST.get('type')
                i_email = request.POST.get('email')
                i_contact = request.POST.get('contact')
                i_state = request.POST.get('state')
                i_city = request.POST.get('city')
                i_pincode = request.POST.get('pincode')

                # updating details
                i = institution_detail.objects.get(id = i_id)
                if i:
                    i.id= i_id
                    i.name=i_name
                    i.type_insti=i_type
                    i.email=i_email
                    i.contact = i_contact
                    i.state = i_state
                    i.city = i_city
                    i.pincode = i_pincode

                    # saving updates to database
                    i.save()
                    messages.success(request, "Successfully updated")
                    return render(request, 'dashboards\dashboard_admin_edit.html')
                else:
                    messages.error(request, "Institution not found.")
                    return render(request, 'dashboards\dashboard_admin_edit.html')

        return render(request, 'dashboards\dashboard_admin_edit.html')
    else:
        return redirect('/login/admin')




def student(request):
    if request.user.is_authenticated:
        uname=request.user.get_username()
        

        user_details = student_detail.objects.filter(sid = uname).values()
        
        
        return render(request, 'dashboards\dashboard_student.html', {'s': user_details[0]})
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

                # generate insti id
                i_id = func.stu_id_gen()

                db_student = student_detail(
                    sid = i_id,
                    name = s_name,
                    dob= dob,
                    guardian_name = guardian,
                    email= email,
                    mobile=contact,
                    aadhar=aadhar,
                    gender=gender,
                    active_status=False,
                    community= community,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode
                )

                db_student.save()
                print('Database Updated :)')

                messages.success(request, "Successfully created student profile.")

                # create student user with no permissions
                User.objects.create_user(
                    username = i_id,
                    email = email,
                    password= 'password',
                )

                print('id:', i_id)


        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        return render(request, 'dashboards\dashboard_institution.html',{'username':uname, 'name':nam, 'email':user_email})
    else:
        return redirect('/login/institution')