from ast import AsyncFunctionDef
import email
from email import message
from email.headerregistry import Address
from signal import SIG_DFL
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from sip_db.models import api_details, institution_detail, student_detail, degree, course, docreq
from util import func
from django.contrib import messages

# ADMIN VIEWS
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
            password = User.objects.make_random_password()

            #generate insti id
            i_id = func.insti_id_gen()

            # must add contact later
            # to send id and pass as email
            if func.insti_creation(i_email,i_id,password):
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
                    first_name = i_name,
                    username = i_id, 
                    email = i_email,
                    password = password,
                    is_staff = True
                )
                #new_user.is_staff = True

                messages.success(request, "Successfully created institution profile.")
                return redirect('/dashboard/admin')
            else:
                messages.error(request, "Something Went Wrong! Try Again After Some Time")
                return redirect('/dashboard/admin')

        # getting username from login
        uname=request.user.get_username()

        # getting other user details in a obj 'user'
        user = User.objects.get(username=uname)
        user_email = user.email
        name = user.get_full_name()
        return render(request, 'dashboards\d_admin\dashboard_admin.html', {'username':uname, 'name':name, 'email':user_email})
    else:
        return redirect('/login/admin')

def admin_search(request):
    if request.user.is_authenticated:
        # getting username from login & getting other user details in a obj 'user'
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        name = user.get_full_name()

        if request.method == "POST":
            if 'search' in request.POST:
                i_id = request.POST.get('institution-id')
                search_details = institution_detail.objects.filter(id = i_id).values()
                # no of students enrolled
                d_details = degree.objects.filter(iid=i_id).values()

                if search_details:
                    return render(request, 'dashboards\d_admin\dashboard_admin_search.html',
                        {'i': search_details[0],'student_count': len(d_details), 'username':uname, 'name':name, 'email':user_email}
                    )
                else:
                    messages.error(request, "Institution not found.")
                    return redirect('/dashboard/admin/search')
        
        return render(request, 'dashboards\d_admin\dashboard_admin_search.html', {'username':uname, 'name':name, 'email':user_email})
    else:
        return redirect('/login/admin')
    
def admin_edit(request):
    if request.user.is_authenticated:
        # getting username from login & getting other user details in a obj 'user'
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        name = user.get_full_name()

        if request.method == "POST":
            # search insti
            if 'search' in request.POST:
                i_id = request.POST.get('institution-id')
                search_details = institution_detail.objects.filter(id = i_id).values()
                if search_details:
                    return render(request, 'dashboards\d_admin\dashboard_admin_edit.html',
                        {'i': search_details[0], 'username':uname, 'name':name, 'email':user_email}
                    )
                else:
                    messages.error(request, "Institution not found.")
                    return redirect('/dashboard/admin/edit')


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
                    return redirect('/dashboard/admin/edit')
                else:
                    messages.error(request, "Institution not found.")
                    return redirect('/dashboard/admin/edit')

        return render(request, 'dashboards\d_admin\dashboard_admin_edit.html', {'username':uname, 'name':name, 'email':user_email})
    else:
        return redirect('/login/admin')


def create_api(request):
    # getting username from login & getting other user details in a obj 'user'
    uname=request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    name = user.get_full_name()

    if request.method == "POST":
        org_name = request.POST.get('organization-name')
        email = request.POST.get('organization-email')
        api_key = func.api_key_gen()
        perm = request.POST.get('type')
        db_instance = api_details(
                org_name = org_name,
                api_key = api_key,
                email = email,
                permissions = perm
            )
        db_instance.save()
        apiid = api_details.objects.filter(email=email).values()
        apiid = apiid[0]['api_id']
        if func.api_mail_creation(email,org_name,api_key, apiid):
            messages.success(request,"API Key Generated Successfully")
        else:
            messages.success(request,"Something Went Wrong Try Again")
            
    return render(request, "dashboards\d_admin\create-api.html", {'username':uname, 'name':name, 'email':user_email})
    
def revok_api(request):
    # getting username from login & getting other user details in a obj 'user'
    uname=request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    name = user.get_full_name()

    if request.method == "POST":
        apiid = request.POST.get('apiid')
        
        a = api_details.objects.filter(api_id = apiid).values()
        print(a)
        if a:
            print('goin into a')
            email = a[0]['email']
            api_details.objects.filter(api_id=apiid).delete()
            func.api_mail_revok(email,apiid)
            messages.success(request, "API Access Revoked")
            
        else:
            messages.error(request, "API ID Not Found")
            return redirect('/dashboard/admin/revokapi')
    
        
        
    return render(request, "dashboards\d_admin\evoke-api.html", {'username':uname, 'name':name, 'email':user_email})


# INSTITUTION VIEWS


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
            password = User.objects.make_random_password()
            
            # generate insti id
            i_id = func.stu_id_gen()

            if func.stu_creation(email,i_id,password):
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

                # create student user with no permissions
                User.objects.create_user(
                    first_name = s_name,
                    username = i_id,
                    email = email,
                    password= password,
                )
                messages.success(request, "Successfully created student profile.")
                return redirect('/dashboard/institution')
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(iid_id=uname, status = 'Pursuing').values())
        return render(request, 'dashboards\institution\dashboard_institution.html',{'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
    else:
        return redirect('/login/institution')

def institution_search(request):
    if request.user.is_authenticated:
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(iid_id=uname, status = 'Pursuing').values())

        if request.method == "POST":
            
            s_id = request.POST.get('stu_id')
            search_details = student_detail.objects.filter(sid = s_id).values()
            
            if search_details:
                return render(request, 'dashboards\institution\dashboard_institution_search.html', {'s': search_details[0], 'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
            else:
                messages.error(request, "Student not found.")
                return redirect('/dashboard/institution/search')
        else:
            return render(request, 'dashboards\institution\dashboard_institution_search.html',{'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
    else:
        return redirect('/login/institution')

def institution_edit(request):
    if request.user.is_authenticated:
        
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(iid_id=uname, status = 'Pursuing').values())

        if request.method == "POST":
            # search student
            if 'search' in request.POST:
                s_id = request.POST.get('s-id')
                search_details = student_detail.objects.filter(sid = s_id).values()
                if search_details:

                    return render(request, 'dashboards\institution\dashboard_institution_edit.html', {'s': search_details[0], 'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
                else:
                    messages.error(request, "Student not found.")
                    return redirect('/dashboard/institution/edit')


            # change student details
            if 'edit' in request.POST:
                s_id = request.POST.get('s-id')
                s_name = request.POST.get('s-name')
                s_dob = request.POST.get('dob')
                s_guardian = request.POST.get('pgname')
                s_email = request.POST.get('email')
                s_mobile = request.POST.get('contact')
                s_aadhar = request.POST.get('aadhar')
                s_gender = request.POST.get('gender')
                s_status = request.POST.get('active_status')
                s_community = request.POST.get('community')
                s_address = request.POST.get('address')
                s_city = request.POST.get('city')
                s_state = request.POST.get('state')
                s_pincode = request.POST.get('pincode')

                #hardcode active status
                s_status = True
                # updating details
                s = student_detail.objects.get(sid = s_id)
                if s:
                    s.name = s_name
                    s.dob= s_dob
                    s.guardian_name = s_guardian
                    s.email= s_email
                    s.mobile= s_mobile
                    s.aadhar= s_aadhar
                    s.gender= s_gender
                    s.active_status= s_status
                    s.community= s_community
                    s.address= s_address
                    s.city= s_city
                    s.state= s_state
                    s.pincode= s_pincode

                    # saving updates to database
                    s.save()
                    messages.success(request, "Successfully updated")
                    return redirect('/dashboard/institution/edit')
                else:
                    messages.error(request, "Student not found.")
                    return redirect('/dashboard/institution/edit')

        
        return render(request, 'dashboards\institution\dashboard_institution_edit.html', {'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
    else:
        return redirect('/login/institution')

def institution_enroll_student(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            s_id = request.POST.get('student-id')
            d_name = request.POST.get('degree-name')
            discipline = request.POST.get('discipline')
            join_year = request.POST.get('joining-year')

            uname=request.user.get_username()
            

            # get instances
            try:
                stu = student_detail.objects.get(sid = s_id)
                ins = institution_detail.objects.get(id = uname)
            except:
                messages.success(request, 'Student ID invalid.')
                return redirect('/dashboard/institution/enroll')

            db_degree = degree(
                sid = stu,
                iid = ins,
                name = d_name,
                status = 'Pursuing',
                discipline = discipline,
                year_join = join_year,
            )
            db_degree.save()

            messages.success(request, 'Successfully enrolled student to institution and degree.')
            return redirect('/dashboard/institution/enroll')
        else:
            uname=request.user.get_username()
            user = User.objects.get(username=uname)
            user_email = user.email
            nam=user.get_full_name()
            # students enrolled
            no_of_stu = len(degree.objects.filter(iid_id=uname, status = 'Pursuing').values())
            return render(request, 'dashboards\institution\dashboard_institution_enroll_student.html', {'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
    else:
        return redirect('/login/institution')

def institution_removestudent(request):
    if request.user.is_authenticated:
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(iid_id=uname, status = 'Pursuing').values())

        if request.method == "POST":
            s_id = request.POST.get('student-id')
            fmark = request.POST.get('final-mark')
            leave_year = request.POST.get('year')
            leave_type = request.POST.get('type')

            try:
                degree_details = degree.objects.get(sid= s_id, iid=uname, status='Pursuing')
            except:
                messages.error(request, 'Student not found.')
                return redirect('/dashboard/institution/remove')

            degree_details.grade = fmark
            degree_details.year_leave = leave_year
            degree_details.status = leave_type
            
            degree_details.save()

            messages.success(request, 'Successfully removed student from institution.')
            return redirect('/dashboard/institution/remove')
        else:          
            
            return render(request, 'dashboards\institution\dashboard_institution_remove_student.html', {'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
    else:
        return redirect('/login/institution')

def institution_addcourse(request):
    if request.user.is_authenticated:
        # get stu id and insti id
        uname=request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam=user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(iid_id=uname, status = 'Pursuing').values())
        if request.method == 'POST':
            s_id = request.POST.get('search-student')

            if 'search' in request.POST:
                
                # get student and institution instances
                try:
                    s_details = student_detail.objects.get(sid = s_id)  
                    i_details = institution_detail.objects.get(id = uname)
                    
                except:
                    messages.error(request, 'Student details invalid.')
                    return redirect('/dashboard/institution/addcourse')
                
                degree_details = degree.objects.get(sid=s_details, iid=i_details, status='Pursuing')
                if degree_details:
                    return render(request, 'dashboards\institution\dashboard_institution_add_course.html',
                        {'username':uname, 'name':nam, 'email':user_email, 'disabled':'disabled', 's':s_details, 'd':degree_details, 'student_count': no_of_stu}
                    )
                else:
                    messages.error(request, 'Student not enrolled in your institution.')
                    return redirect('/dashboard/institution/addcourse')
            elif 'add' in request.POST:
                
                # get student and institution instances
                s_details = student_detail.objects.get(sid = s_id)  
                i_details = institution_detail.objects.get(id = uname)
                degree_details = degree.objects.get(sid=s_details, iid=i_details)
                if degree_details:
                    pass
                else:
                    messages.error(request, 'Student not enrolled in your institution 2')
                    return redirect('/dashboard/institution/addcourse')
                
                # get details
                course_name = request.POST.get('course-name')
                t_name = request.POST.get('total-mark')
                o_name = request.POST.get('total-mark')
                credits = request.POST.get('credits')
                sem = request.POST.get('semester')


                # save details in database
                db_course = course(
                    did =degree_details,
                    name = course_name,
                    total_marks = t_name,
                    obtained_marks = o_name,
                    credits = credits,
                    semester = sem,
                )
                db_course.save()
                print('success')
                messages.success(request, 'Successfully created course in degree')
                return redirect('/dashboard/institution/addcourse')
        else:
            return render(request, 'dashboards\institution\dashboard_institution_add_course.html', {'username':uname, 'name':nam, 'email':user_email, 'student_count': no_of_stu})
    else:
        return redirect('/login/institution')


# STUDENT VIEWS

def student(request):
    if request.user.is_authenticated:
        uname=request.user.get_username()
        user_details = student_detail.objects.filter(sid = uname).values()
        
        degree_details = degree.objects.filter(sid=uname).values()
        
        i_details=[]
        for d in degree_details:
            i_id = d['iid_id']
            ins = institution_detail.objects.get(id=i_id)
            i_details.append(ins)


        if user_details:
            return render(request, 'dashboards\student\dashboard_student.html', {'s': user_details[0], 'i':i_details})
        else:
            return render(request, 'dashboards\student\dashboard_student.html')
    else:
        return redirect('/login/student')

def student_get_docu(request):
    if request.user.is_authenticated:
        uname=request.user.get_username()
        # create user and degree instances
        user_details = student_detail.objects.filter(sid = uname).values()
        degree_details = degree.objects.filter(sid=uname).values()
        
        # searching insti where student is studying the degree
        i_details=[]
        for i in range(len(degree_details)):
            temp = degree_details[i]
            i_details.append(institution_detail.objects.get(id= temp['iid_id']))
        
        if request.method=='POST':
            
            doc_type = request.POST.get('document-type')
            i_id = request.POST.get('institution')
            reason = request.POST.get('reason')

            # creating instances
            stu = student_detail.objects.get(sid=uname)
            ins = institution_detail.objects.get(id=i_id)
            doc_db = docreq(
                sid=stu,
                i_id=ins,
                doc_type=doc_type,
                reason=reason,
                status='Pending',
            )
            doc_db.save()

            messages.success(request, 'Successfully requested.')
            return render(request, 'dashboards\student\dashboard_student_document.html', {'s': user_details[0]})
            
        return render(request, 'dashboards\student\dashboard_student_document.html', {'s': user_details[0], 'd': i_details})
    else:
        return redirect('/login/student')

