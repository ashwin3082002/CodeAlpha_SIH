from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from sip_db.models import api_details, institution_detail, student_detail, degree, course, docreq, account_detail
from util import func
from django.contrib import messages
import pandas as pd

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

            # generate insti id
            i_id = func.insti_id_gen()

            # must add contact later
            # to send id and pass as email
            if func.insti_creation(i_email, i_id, password):
                # database instance
                db_insti = institution_detail(
                    id=i_id,
                    name=i_name,
                    type_insti=i_type,
                    email=i_email,
                    contact=i_contact,
                    state=i_state,
                    city=i_city,
                    pincode=i_pincode,
                )
                db_insti.save()

                # create new user and grant staff status
                User.objects.create_user(
                    first_name=i_name,
                    username=i_id,
                    email=i_email,
                    password=password,
                    is_staff=True
                )
                
                #new_user.is_staff = True
                # upload pic
                try:
                    if request.FILES['profilepic']:
                        pic = request.FILES['profilepic']
                        db_insti.profile_pic = pic
                        db_insti.save()
                except:
                    pass

                messages.success(
                    request, "Successfully created institution profile.")
                return redirect('/dashboard/admin')
            else:
                messages.error(
                    request, "Something Went Wrong! Try Again After Some Time")
                return redirect('/dashboard/admin')

        # getting username from login
        uname = request.user.get_username()

        # getting other user details in a obj 'user'
        user = User.objects.get(username=uname)
        user_email = user.email
        name = user.get_full_name()
        return render(request, 'dashboards/d_admin/dashboard_admin.html', {'username': uname, 'name': name, 'email': user_email})
    else:
        return redirect('/login/admin')


def admin_bulk(request):
    if request.user.is_authenticated:
        if request.method == "POST" and request.FILES['myfile']:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(f"{uname+'_bulkaddstu'}.csv", myfile)
            messages.success(request, f"File Uploaded")
            filepath = fs.path(filename)
            df = pd.read_csv(f"{filepath}")

            for i in range(len(df)):
                i_name = df.iloc[i, 0]
                i_type = df.iloc[i, 1]
                i_email = df.iloc[i, 2]
                i_contact = df.iloc[i, 3]
                i_state = df.iloc[i, 4]
                i_city = df.iloc[i, 5]
                i_pincode = df.iloc[i, 6]

                # generate insti id and pass
                i_id = func.insti_id_gen()
                password = User.objects.make_random_password()

                # to send id and pass as email
                if func.insti_creation(i_email, i_id, password):
                    # database instance
                    db_insti = institution_detail(
                        id=i_id,
                        name=i_name,
                        type_insti=i_type,
                        email=i_email,
                        contact=i_contact,
                        state=i_state,
                        city=i_city,
                        pincode=i_pincode,
                    )
                    db_insti.save()

                    # create new user and grant staff status
                    User.objects.create_user(
                        first_name=i_name,
                        username=i_id,
                        email=i_email,
                        password=password,
                        is_staff=True
                    )
                else:
                    messages.error(
                        request, "Something Went Wrong! Try Again After Some Time")
                    return redirect('/dashboard/admin/bulk')
            fs.delete(filename)
            messages.success(
                request, "Successfully created institution profiles.")
            return redirect('/dashbord/admin/bulk')

        # getting username from login
        uname = request.user.get_username()

        # getting other user details in a obj 'user'
        user = User.objects.get(username=uname)
        user_email = user.email
        name = user.get_full_name()
        return render(request, 'dashboards/d_admin/dash_bulk_create.html', {'username': uname, 'name': name, 'email': user_email})
    else:
        return redirect('/login/admin')


def admin_search(request):
    if request.user.is_authenticated:
        # getting username from login & getting other user details in a obj 'user'
        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        name = user.get_full_name()

        if request.method == "POST":
            if 'search' in request.POST:
                i_id = request.POST.get('institution-id')
                search_details = institution_detail.objects.filter(
                    id=i_id).values()
                # no of students enrolled
                d_details = degree.objects.filter(iid=i_id).values()

                if search_details:
                    return render(request, 'dashboards/d_admin/dashboard_admin_search.html',
                                  {'i': search_details[0], 'student_count': len(
                                      d_details), 'username': uname, 'name': name, 'email': user_email}
                                  )
                else:
                    messages.error(request, "Institution not found.")
                    return redirect('/dashboard/admin/search')

        return render(request, 'dashboards/d_admin/dashboard_admin_search.html', {'username': uname, 'name': name, 'email': user_email})
    else:
        return redirect('/login/admin')


def admin_edit(request):
    if request.user.is_authenticated:
        # getting username from login & getting other user details in a obj 'user'
        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        name = user.get_full_name()

        if request.method == "POST":
            # search insti
            if 'search' in request.POST:
                i_id = request.POST.get('institution-id')
                search_details = institution_detail.objects.filter(
                    id=i_id).values()
                if search_details:
                    return render(request, 'dashboards/d_admin/dashboard_admin_edit.html',
                                  {'i': search_details[0], 'username': uname,
                                      'name': name, 'email': user_email}
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
                i = institution_detail.objects.get(id=i_id)
                if i:
                    i.id = i_id
                    i.name = i_name
                    i.type_insti = i_type
                    i.email = i_email
                    i.contact = i_contact
                    i.state = i_state
                    i.city = i_city
                    i.pincode = i_pincode
                    # upload pic
                    if request.FILES['profilepic']:
                        pic = request.FILES['profilepic']
                        i.profile_pic = pic
                    # saving updates to database
                    i.save()
                    messages.success(request, "Successfully updated.")
                    return redirect('/dashboard/admin/edit')
                else:
                    messages.error(request, "Institution not found.")
                    return redirect('/dashboard/admin/edit')

        return render(request, 'dashboards/d_admin/dashboard_admin_edit.html', {'username': uname, 'name': name, 'email': user_email})
    else:
        return redirect('/login/admin')


def create_api(request):
    # getting username from login & getting other user details in a obj 'user'
    uname = request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    name = user.get_full_name()

    if request.method == "POST":
        org_name = request.POST.get('organization-name')
        email = request.POST.get('organization-email')
        api_key = func.api_key_gen()
        perm = request.POST.get('type')
        db_instance = api_details(
            org_name=org_name,
            api_key=api_key,
            email=email,
            permissions=perm
        )
        db_instance.save()
        apiid = api_details.objects.filter(email=email).values()
        apiid = apiid[0]['api_id']
        if func.api_mail_creation(email, org_name, api_key, apiid):
            messages.success(request, "API Key Generated Successfully")
        else:
            messages.success(request, "Something Went Wrong Try Again")

    return render(request, "dashboards/d_admin/create-api.html", {'username': uname, 'name': name, 'email': user_email})


def revok_api(request):
    # getting username from login & getting other user details in a obj 'user'
    uname = request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    name = user.get_full_name()

    if request.method == "POST":
        apiid = request.POST.get('apiid')

        a = api_details.objects.filter(api_id=apiid).values()
        if a:
            email = a[0]['email']
            api_details.objects.filter(api_id=apiid).delete()
            func.api_mail_revok(email, apiid)
            messages.success(request, "API Access Revoked")

        else:
            messages.error(request, "API ID Not Found")
            return redirect('/dashboard/admin/revokapi')

    return render(request, "dashboards/d_admin/evoke-api.html", {'username': uname, 'name': name, 'email': user_email})


def reports(request):
    # getting username from login & getting other user details in a obj 'user'
    uname = request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    name = user.get_full_name()
    return render(request, "dashboards/d_admin/eports_admin.html", {'username': uname, 'name': name, 'email': user_email})


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

            # generate insti id and password
            i_id = func.stu_id_gen()
            password = User.objects.make_random_password()

            if func.stu_creation(email, i_id, password):
                db_student = student_detail(
                    sid=i_id,
                    name=s_name,
                    dob=dob,
                    guardian_name=guardian,
                    email=email,
                    mobile=contact,
                    aadhar=aadhar,
                    gender=gender,
                    active_status=False,
                    community=community,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode
                )

                db_student.save()

                # create student user with no permissions
                User.objects.create_user(
                    first_name=s_name,
                    username=i_id,
                    email=email,
                    password=password,
                )

                # upload pic
                try:
                    if request.FILES['profilepic']:
                        pic = request.FILES['profilepic']
                        db_student.profile_pic = pic
                        db_student.save()
                except:
                    pass

                messages.success(
                    request, "Successfully created student profile.")
                return redirect('/dashboard/institution')
        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam = user.get_full_name()

        # profile pic
        try:
            ins_pp = institution_detail.objects.get(id=uname).profile_pic
        except:
            return redirect('/login/institution')
        # students enrolled
        no_of_stu = len(degree.objects.filter(
            iid_id=uname, status='Pursuing').values())
        return render(request, 'dashboards/institution/dashboard_institution.html', {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
    else:
        return redirect('/login/institution')


def institution_createbulk(request):

    uname = request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    nam = user.get_full_name()

    # students enrolled
    no_of_stu = len(degree.objects.filter(
        iid_id=uname, status='Pursuing').values())

    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(f"{uname+'_bulkaddstu'}.csv", myfile)
        messages.success(request, f"File Uploaded")
        filepath = fs.path(filename)
        df = pd.read_csv(f"{filepath}")
        for i in range(len(df)):

            s_name = df.iloc[i, 0]
            dob = df.iloc[i, 1]
            guardian = df.iloc[i, 2]
            aadhar = df.iloc[i, 3]
            gender = df.iloc[i, 4]
            email = df.iloc[i, 5]
            contact = df.iloc[i, 6]
            address = df.iloc[i, 7]
            city = df.iloc[i, 8]
            state = df.iloc[i, 9]
            pincode = df.iloc[i, 10]
            # generate password
            password = User.objects.make_random_password()

            # generate insti id
            i_id = func.stu_id_gen()

            # profile creation
            if True:
                db_student = student_detail(
                    sid=i_id,
                    name=s_name,
                    dob=dob,
                    guardian_name=guardian,
                    email=email,
                    mobile=contact,
                    aadhar=aadhar,
                    gender=gender,
                    active_status=False,
                    community="General",
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode
                )

                db_student.save()

                # create student user with no permissions
                User.objects.create_user(
                    first_name=s_name,
                    username=i_id,
                    email=email,
                    password=password,
                )

            else:
                messages.error(request, f"Cannot create {s_name}/'s profile.")
                return redirect('/dashboard/institution/create/bulk')

        fs.delete(filename)
        messages.success(
            request, 'The student profiles have been created successfully')
        return redirect('/dashboard/institution/create/bulk')
    try:
        ins_pp = institution_detail.objects.get(id=uname).profile_pic
    except:
        return redirect('/login/institution')
    return render(request, "dashboards/institution/dash_bulk_createstudent.html", {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })


def institution_search(request):

    if request.user.is_authenticated:
        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam = user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(
            iid_id=uname, status='Pursuing').values())
        try:
            ins_pp = institution_detail.objects.get(id=uname).profile_pic
        except:
            return redirect('/login/institution')
        if request.method == "POST":

            s_id = request.POST.get('stu_id')
            search_details = student_detail.objects.filter(sid=s_id).values()

            if search_details:
                return render(request, 'dashboards/institution/dashboard_institution_search.html', {'s': search_details[0], 'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
            else:
                messages.error(request, "Student not found.")
                return redirect('/dashboard/institution/search')
        else:

            return render(request, 'dashboards/institution/dashboard_institution_search.html', {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
    else:
        return redirect('/login/institution')


def institution_edit(request):

    if request.user.is_authenticated:

        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam = user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(
            iid_id=uname, status='Pursuing').values())

        try:
            ins_pp = institution_detail.objects.get(id=uname).profile_pic
        except:
            return redirect('/login/institution')
        if request.method == "POST":
            # search student
            if 'search' in request.POST:
                s_id = request.POST.get('s-id')
                search_details = student_detail.objects.filter(
                    sid=s_id).values()
                if search_details:

                    return render(request, 'dashboards/institution/dashboard_institution_edit.html', {'s': search_details[0], 'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
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

                # hardcode active status
                s_status = True
                # updating details
                s = student_detail.objects.get(sid=s_id)
                if s:
                    s.name = s_name
                    s.dob = s_dob
                    s.guardian_name = s_guardian
                    s.email = s_email
                    s.mobile = s_mobile
                    s.aadhar = s_aadhar
                    s.gender = s_gender
                    s.active_status = s_status
                    s.community = s_community
                    s.address = s_address
                    s.city = s_city
                    s.state = s_state
                    s.pincode = s_pincode

                    # saving updates to database
                    s.save()

                    # upload pic
                    if request.FILES['profilepic']:
                        pic = request.FILES['profilepic']
                        s.profile_pic = pic
                        s.save()
                    messages.success(request, "Successfully updated.")
                    return redirect('/dashboard/institution/edit')
                else:
                    messages.error(request, "Student not found.")
                    return redirect('/dashboard/institution/edit')

        return render(request, 'dashboards/institution/dashboard_institution_edit.html', {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
    else:
        return redirect('/login/institution')


def institution_enroll_student(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            s_id = request.POST.get('student-id')
            d_name = request.POST.get('degree-name')
            discipline = request.POST.get('discipline')
            join_year = request.POST.get('joining-year')

            uname = request.user.get_username()

            # get instances
            try:
                stu = student_detail.objects.get(sid=s_id)
                ins = institution_detail.objects.get(id=uname)
            except:
                messages.success(request, 'Student ID invalid.')
                return redirect('/dashboard/institution/enroll')

            # setting student profile to studying status
            if stu.active_status != True:
                stu.active_status = True
                stu.save()

            db_degree = degree(
                sid=stu,
                iid=ins,
                name=d_name,
                status='Pursuing',
                discipline=discipline,
                year_join=join_year,
            )
            db_degree.save()

            messages.success(
                request, 'Successfully enrolled student to institution and degree.')
            return redirect('/dashboard/institution/enroll')
        else:

            uname = request.user.get_username()
            user = User.objects.get(username=uname)
            user_email = user.email
            nam = user.get_full_name()
            # students enrolled
            no_of_stu = len(degree.objects.filter(
                iid_id=uname, status='Pursuing').values())

            deg = degree.objects.filter(iid=uname).values

            try:
                ins_pp = institution_detail.objects.get(id=uname).profile_pic
            except:
                return redirect('/login/institution')
            return render(request, 'dashboards/institution/dashboard_institution_enroll_student.html', {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, 'deg': deg})
    else:
        return redirect('/login/institution')


def institution_enroll_bulk(request):

    uname = request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    nam = user.get_full_name()

    # students enrolled
    no_of_stu = len(degree.objects.filter(
        iid_id=uname, status='Pursuing').values())

    try:
        ins_pp = institution_detail.objects.get(id=uname).profile_pic
    except:
        return redirect('/login/institution')

    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(f"{uname+'_bulkaddstu'}.csv", myfile)
        messages.success(request, f"File Uploaded")
        filepath = fs.path(filename)
        df = pd.read_csv(f"{filepath}")
        for i in range(len(df)):

            sid = df.iloc[i, 0]
            d_name = df.iloc[i, 1]
            discipline = df.iloc[i, 2]
            join_year = df.iloc[i, 3]
            try:
                stu = student_detail.objects.get(sid=sid)
                ins = institution_detail.objects.get(id=uname)
            except:
                messages.error(request, f'Student ID: {sid} not valid')
                return redirect('/dashboard/institution/enroll/bulk')

            # setting student profile to studying status
            if stu.active_status != True:
                stu.active_status = True
                stu.save()

            # insert data into db
            db_degree = degree(
                sid=stu,
                iid=ins,
                name=d_name,
                status='Pursuing',
                discipline=discipline,
                year_join=join_year,
            )
            db_degree.save()

        fs.delete(filename)
        messages.success(
            request, 'The students have been enrolled successfully')

        return redirect('/dashboard/institution/enroll/bulk')
    return render(request, "dashboards/institution/dash_bulk_enrollstudent.html", {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })


def institution_removestudent(request):

    if request.user.is_authenticated:
        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam = user.get_full_name()

        # students enrolled
        no_of_stu = len(degree.objects.filter(
            iid_id=uname, status='Pursuing').values())

        try:
            ins_pp = institution_detail.objects.get(id=uname).profile_pic
        except:
            return redirect('/login/institution')

        if request.method == "POST":
            s_id = request.POST.get('student-id')
            fmark = request.POST.get('final-mark')
            leave_year = request.POST.get('year')
            leave_type = request.POST.get('type')

            try:
                degree_details = degree.objects.get(
                    sid=s_id, iid=uname, status='Pursuing')
            except:
                messages.error(request, 'Student not found.')
                return redirect('/dashboard/institution/remove')

            degree_details.grade = fmark
            degree_details.year_leave = leave_year
            degree_details.status = leave_type

            degree_details.save()

            d = degree.objects.filter(sid=s_id, status='Pursuing').values()

            if len(d) == 0:
                stu = student_detail.objects.get(sid=s_id)
                stu.active_status = False
                stu.save()

            messages.success(
                request, 'Successfully removed student from institution.')
            return redirect('/dashboard/institution/remove')
        else:

            return render(request, 'dashboards/institution/dashboard_institution_remove_student.html', {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
    else:
        return redirect('/login/institution')


def institution_removestudent_bulk(request):

    uname = request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    nam = user.get_full_name()

    # students enrolled
    no_of_stu = len(degree.objects.filter(
        iid_id=uname, status='Pursuing').values())

    try:
        ins_pp = institution_detail.objects.get(id=uname).profile_pic
    except:
        return redirect('/login/institution')
    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(f"{uname+'_bulkaddstu'}.csv", myfile)
        messages.success(request, f"File Uploaded")
        filepath = fs.path(filename)
        df = pd.read_csv(f"{filepath}")

        for i in range(len(df)):
            sid = df.iloc[i, 0]
            fmark = df.iloc[i, 1]
            leave_year = df.iloc[i, 2]
            leave_type = df.iloc[i, 3]

            try:
                degree_details = degree.objects.get(
                    sid=sid, iid=uname, status='Pursuing')
            except:
                messages.error(request, 'Student not found.')
                return redirect('/dashboard/institution/remove/bulk')

            # insert data into db
            degree_details.grade = fmark
            degree_details.year_leave = leave_year
            degree_details.status = leave_type
            degree_details.save()

        fs.delete(filename)
        messages.success(request, 'The student profiles have successfully')

        return redirect('/dashboard/institution/create/bulk')
    return render(request, "dashboards/institution/dash_bulk_enrollstudent.html", {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })


def institution_addcourse(request):

    if request.user.is_authenticated:
        # get stu id and insti id
        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam = user.get_full_name()
        # students enrolled
        no_of_stu = len(degree.objects.filter(
            iid_id=uname, status='Pursuing').values())
        try:
            ins_pp = institution_detail.objects.get(id=uname).profile_pic
        except:
            return redirect('/login/institution')
        if request.method == 'POST':
            s_id = request.POST.get('search-student')

            if 'search' in request.POST:

                # get student and institution instances
                try:
                    s_details = student_detail.objects.get(sid=s_id)
                    i_details = institution_detail.objects.get(id=uname)

                except:
                    messages.error(request, 'Student details invalid.')
                    return redirect('/dashboard/institution/addcourse')

                degree_details = degree.objects.filter(
                    sid=s_details, iid=i_details, status='Pursuing').values()
                if degree_details:
                    return render(request, 'dashboards/institution/dashboard_institution_add_course.html',
                                  {'username': uname, 'name': nam, 'email': user_email, 'disabled': 'disabled',
                                      's': s_details, 'd': degree_details[0], 'student_count': no_of_stu, 'pp': ins_pp, }
                                  )
                else:
                    messages.error(
                        request, 'Student not enrolled in your institution.')
                    return redirect('/dashboard/institution/addcourse')
            elif 'add' in request.POST:

                # get student and institution instances
                s_details = student_detail.objects.get(sid=s_id)
                i_details = institution_detail.objects.get(id=uname)
                degree_details = degree.objects.get(
                    sid=s_details, iid=i_details, status='Pursuing')
                if degree_details:
                    pass
                else:
                    messages.error(
                        request, 'Student not enrolled in your institution 2')
                    return redirect('/dashboard/institution/addcourse')

                # get details
                course_name = request.POST.get('course-name')
                t_marks = request.POST.get('total-mark')
                o_marks = request.POST.get('total-mark')
                credits = request.POST.get('credits')
                sem = request.POST.get('semester')

                # save details in database
                db_course = course(
                    did=degree_details,
                    name=course_name,
                    total_marks=t_marks,
                    obtained_marks=o_marks,
                    credits=credits,
                    semester=sem,
                )
                db_course.save()
                messages.success(
                    request, 'Successfully created course in degree')

                return redirect('/dashboard/institution/addcourse')
        else:
            return render(request, 'dashboards/institution/dashboard_institution_add_course.html', {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
    else:
        return redirect('/login/institution')


def institution_addcourse_bulk(request):

    uname = request.user.get_username()
    user = User.objects.get(username=uname)
    user_email = user.email
    nam = user.get_full_name()
    # students enrolled
    no_of_stu = len(degree.objects.filter(
        iid_id=uname, status='Pursuing').values())

    try:
        ins_pp = institution_detail.objects.get(id=uname).profile_pic
    except:
        return redirect('/login/institution')

    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(f"{uname+'_bulkaddstu'}.csv", myfile)
        messages.success(request, f"File Uploaded")
        filepath = fs.path(filename)
        df = pd.read_csv(f"{filepath}")
        for i in range(len(df)):
            sid = df.iloc[i, 0]
            did = df.iloc[i, 1]
            course_name = df.iloc[i, 2]
            t_marks = df.iloc[i, 3]
            o_marks = df.iloc[i, 4]
            credit = df.iloc[i, 5]
            sem = df.iloc[i, 6]
            try:
                d_details = degree.objects.get(id=did)
            except:
                messages.error(f'Degree ID: {did} not valid')
                return redirect('/dashboard/institution/addcourse/bulk')
            # insert data into db
            db_course = course(
                did=d_details,
                name=course_name,
                total_marks=t_marks,
                obtained_marks=o_marks,
                credits=credit,
                semester=sem,
            )
            db_course.save()

        fs.delete(filename)

    return render(request, "dashboards/institution/dash_bulk_addcourse.html", {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })


def institution_docreq(request):

    if request.user.is_authenticated:
        uname = request.user.get_username()
        user = User.objects.get(username=uname)
        user_email = user.email
        nam = user.get_full_name()

        # students enrolled
        no_of_stu = len(degree.objects.filter(
            iid_id=uname, status='Pursuing').values())

        try:
            ins_pp = institution_detail.objects.get(id=uname).profile_pic
        except:
            return redirect('/login/institution')

        if request.method == "POST":
            if 'search' in request.POST:
                status = request.POST.get('status')
                doc = docreq.objects.filter(i_id=uname, status=status).values()

                for i in doc:
                    s_id = i['sid_id']
                    i_id = i['i_id_id']

                    # degree instance
                    degree_details = degree.objects.filter(
                        sid=s_id, iid=i_id, status='Pursuing').values()
                    if degree_details:
                        pass
                    else:
                        doc.remove(i)

                if doc:

                    return render(request, 'dashboards/institution/dash_doc.html',
                                  {'username': uname,
                                   'name': nam,
                                   'email': user_email,
                                   'student_count': no_of_stu,
                                   'pp': ins_pp,
                                   'docrequest': doc,
                                   }
                                  )
                else:
                    messages.error(request, 'No records found.')
                    return redirect('/dashboard/institution/docreq')

            elif 'accept' in request.POST:
                doc_id = request.POST.get('doc-id')
                try:
                    doc = docreq.objects.get(id=doc_id)
                except:
                    messages.error(request, 'Invalid Document ID.')
                    return redirect('/dashboard/institution/docreq')
                stu = student_detail.objects.get(sid=doc.sid_id)
                deg_details = degree.objects.filter(
                    sid=doc.sid, iid=doc.i_id, status='Pursuing').values()
                ins_details = institution_detail.objects.get(id=doc.i_id_id)
                deg = deg_details[0]['name']
                try:
                    mobile=stu.mobile
                except:
                    pass
                # send mail
                if doc.doc_type == 'bonafide':
                    func.bonafide_mail(stu.email, stu.name,
                                       stu.guardian_name, deg, ins_details.name,mobile)
                elif doc.doc_type == 'noc':
                    func.noc_mail(stu.email, stu.name,
                                  stu.guardian_name, deg, ins_details.name)
                else:
                    print("exception")
                doc.status = 'Accepted'
                doc.save()
                messages.success(request, 'Document request accepted!')
                return redirect('/dashboard/institution/docreq')

            elif 'reject' in request.POST:
                doc_id = request.POST.get('doc-id')

                try:
                    doc = docreq.objects.get(id=doc_id)
                except:
                    messages.error(request, 'Invalid Document ID.')

                stu = student_detail.objects.get(sid=doc.sid_id)
                func.doc_rej(stu.email)
                doc.status = 'Rejected'
                doc.save()
                messages.success(request, 'Document request rejected!')
                return redirect('/dashboard/institution/docreq')

        return render(request, 'dashboards/institution/dash_doc.html', {'username': uname, 'name': nam, 'email': user_email, 'student_count': no_of_stu, 'pp': ins_pp, })
    else:
        return redirect('/login/institution')


# STUDENT VIEWS

def student(request):
    if request.user.is_authenticated:
        uname = request.user.get_username()
        user_details = student_detail.objects.filter(sid=uname).values()

        degree_details = degree.objects.filter(sid=uname).values()

        i_details = set()
        for d in degree_details:
            i_id = d['iid_id']
            ins = institution_detail.objects.get(id=i_id)
            i_details.add(ins)

        bank_details = account_detail.objects.filter(sid=uname).values()

        if bank_details:
            bool_bank = True
            return render(request, 'dashboards/student/dashboard_student.html', {
                's': user_details[0],
                'i': i_details,
                'd': degree_details,
                'bank': bank_details[0],
                'bank_dis': bool_bank
            })
        else:
            bool_bank = False
            return render(request, 'dashboards/student/dashboard_student.html', {
                's': user_details[0],
                'i': i_details,
                'd': degree_details,
                'bank_dis': bool_bank
            })
    else:
        return redirect('/login/student')


def student_get_docu(request):
    if request.user.is_authenticated:
        uname = request.user.get_username()
        # create user and degree instances
        user_details = student_detail.objects.filter(sid=uname).values()
        degree_details = degree.objects.filter(
            sid=uname, status='Pursuing').values()

        # searching insti where student is studying the degree
        i_details = []
        for i in range(len(degree_details)):
            temp = degree_details[i]
            i_details.append(institution_detail.objects.get(id=temp['iid_id']))

        if request.method == 'POST':
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
            return render(request, 'dashboards/student/dashboard_student_document.html', {'s': user_details[0], 'd': i_details})
        else:
            return render(request, 'dashboards/student/dashboard_student_document.html', {'s': user_details[0], 'd': i_details})
    else:
        return redirect('/login/student')


def bankaccount(request):
    sid = request.session['sid']
    user_details = student_detail.objects.filter(sid=sid).values()
    if request.method == "POST":
        if 'otp' in request.POST:
            bank_name = request.POST.get('bank_name')
            branch = request.POST.get('branch')
            acc_num = request.POST.get('acc_num')
            name = request.POST.get('name')
            ifsc = request.POST.get('ifsc')
            acc = {
                'bank_name': bank_name,
                'branch': branch,
                'acc_num': acc_num,
                'name': name,
                'ifsc': ifsc
            }
            request.session['bank_details'] = acc
            email = user_details[0]['email']
            try:
                mobile = user_details[0]['mobile']
            except:
                pass
            otp = func.sendotp(email, mobile)
            messages.success(request, "OTP Sent")
            request.session['otp'] = otp
            return render(request, 'dashboards/student/ccount_bank.html', {'s': user_details[0], 'var': 'enabled', 'acc': acc, 'var1': 'disabled'})
        elif 'submit' in request.POST:
            u_otp = eval(request.POST.get('otp_check'))
            if u_otp == request.session['otp']:
                # create instance
                try:
                    b_details = account_detail.objects.get(sid=sid)
                    bank_details = request.session['bank_details']
                    b_details.holder_name = bank_details['name']
                    b_details.acc_number = bank_details['acc_num']
                    b_details.bank_name = bank_details['bank_name']
                    b_details.branch_name = bank_details['branch']
                    b_details.ifsc = bank_details['ifsc']
                    b_details.save()
                    messages.success(request, "Details Updated")
                    return redirect("/dashboard/student")
                except:
                    s_details = student_detail.objects.get(sid=sid)
                    bank_details = request.session['bank_details']

                    db_instance = account_detail(
                        sid=s_details,
                        holder_name=bank_details['name'],
                        acc_number=bank_details['acc_num'],
                        bank_name=bank_details['bank_name'],
                        branch_name=bank_details['branch'],
                        ifsc=bank_details['ifsc']
                    )
                    db_instance.save()
                    messages.success(request, "Details Saved")
                    return redirect("/dashboard/student")
            else:
                messages.error(request, 'Wrong OTP')

    return render(request, 'dashboards/student/ccount_bank.html', {'s': user_details[0], 'var': 'disabled'})


def profiledownload(request):
    if request.user.is_authenticated:
        uname = request.user.get_username()
        # student details
        s_detail = student_detail.objects.get(sid=uname)

        # degree details
        d_detail = degree.objects.filter(sid=uname).values()

        # get insti name and append to degree details
        for d in d_detail:
            i = institution_detail.objects.get(id = d['iid_id'])
            d['iname']=i.name

        return render(request, 'dashboards/student/student_report.html', {'s': s_detail, 'degree_data': d_detail})

    else:
        return redirect('/login/student')


def student_courses(request):
    try:
        uname = request.user.get_username()
        user_details = student_detail.objects.get(sid=uname)

        deg = degree.objects.filter(sid=uname).values()
        d = deg[0]
        insti = institution_detail.objects.get(id=d['iid_id'])
        courses = course.objects.filter(did=d['id']).values()
    except:
        messages.error(request, 'Something went wrong! Try Again.')
        return redirect('dashboard/student/courses')

    if request.user.is_authenticated:
        return render(request, 'dashboards/student/dash_courses.html', {'s': user_details, 'c': courses, 'd': d, 'i': insti})
    else:
        return redirect('/login/student')


def scholarship(request):
    uname = request.user.get_username()
    user_details = student_detail.objects.get(sid=uname)

    if request.user.is_authenticated:
        return render(request, 'dashboards/student/scholarship.html', {'s': user_details})
    else:
        return redirect('/login/student')
