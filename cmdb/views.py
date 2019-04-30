from django.shortcuts import render
from django.shortcuts import HttpResponse
from cmdb import models
from datetime import datetime
import json
from cmdb import charts as ch
import hashlib
import uuid
from dateutil import parser
import random
from django.db import connection
from django.utils import timezone
import pytz

from cmdb import report as rep
from io import BytesIO
#from django.http import HttpResponse
import xhtml2pdf.pisa as pisa


def hash_text(text):
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest()


def hash_password(password):
    # taken from https://www.pythoncentral.io/hashing-strings-with-python/
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    # taken from https://www.pythoncentral.io/hashing-strings-with-python/
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


# Create your views here.


user_list = [
    {"user":"jack","pwd":"abc"},
    {"user":"wom","pwd":"ABC"},
]







# def charts_filter(request):
#     type =
#     start_date, end_date = "01/01/2008", "12/31/2019"
#     hscript, hdiv,tscript,tdiv = ch.generate_charts(start_date,end_date,assig_type = [type])#modules = ["COM1003", "COM4502","COM6009"])  #,levels = ["PGT"])
#     return render(request,"charts.html",{"hscript":hscript,"hdiv":hdiv,"tscript":tscript,"tdiv":tdiv})


def index(request):
    # pass


    # if request.method == "POST":
    #     return render(request, "registration.html", )



    return render(request, "index.html",)


def registration(request):

    if request.method == "POST":
        identity = request.POST.get("identity", None)
        email = request.POST.get("email", None)
        id = hash_text(email)
        # id = request.POST.get("id", None)
        password = request.POST.get("pswl", None)
        realname = request.POST.get("realname", None)
        position = request.POST.get("pos", None)
        encripted_pwd = hash_password(password)
        # 添加数据到数据库
        if identity == "0":
            if len(models.Academics.objects.filter(academic_id=id))>0:
                return render(request, "used.html",)
            elif len(models.Academics.objects.filter(email=email))>0:
                return render(request, "used.html", )
            else:
                models.Academics.objects.create(academic_id=id,email=email,name=realname, encripted_pwd=encripted_pwd)
                return render(request, "registration.html", {"note": "registration complete!"})
        else:
            if len(models.Administrators.objects.filter(admin_id=id))>0:
                return render(request, "used.html",)
            elif len(models.Administrators.objects.filter(email=email))>0:
                return render(request, "used.html",)
            else:
                models.Administrators.objects.create(admin_id=id, position=position,email=email,name=realname, encripted_pwd=encripted_pwd)
                return render(request, "index.html", {"note": "registration complete!"})
    return render(request, "registration.html", {"note": ""})


def moduleadd(request):
    if request.method == "POST":
        name = request.POST.get("uName",None)
        module_code = request.POST.get("mCode", None)
        academic_id = models.Academics.objects.get(name=name).academic_id
        department = request.POST.get("department", None)
        duration = request.POST.get("duration", None)
        students = request.POST.get("sNumber", None)
        credits = request.POST.get("credit", None)
        level = request.POST.get("Lever", None)
        module_id = hash_text(module_code+academic_id+duration)
        if len(models.Modules.objects.filter(module_code=module_code))>0:
            return render(request, "used.html", )
        else:
            models.Modules.objects.create(module_id=module_id,module_code=module_code, academic_id=academic_id, department=department,
                                          duration=duration, students=students, credits=credits,level=level)
        model_list = models.Modules.objects.filter(academic_id=academic_id)
        data = []
        for a in model_list:
            data.append(a.module_code)
        return render(request, "mainpart.html", {"data": data, "name": name})


#  下面这个是点击module进行更改的跳转function
def moduleinfo_edit(request):
    if request.method == "POST":
        email = request.session.get('member_id')
        academic_id=models.Academics.objects.get(email=email).academic_id
        model_code=request.POST.get("submit",None)
        module_id = models.Modules.objects.get(module_code=model_code,academic_id=academic_id).module_id
        request.session['moduleid'] = model_code
        credits = models.Modules.objects.get(module_id=module_id).credits
        department = models.Modules.objects.get(module_id=module_id).department
        duration = models.Modules.objects.get(module_id=module_id).duration
        students = models.Modules.objects.get(module_id=module_id).students
        id = models.Modules.objects.get(module_id=module_id).academic_id
        uname = models.Academics.objects.get(academic_id=id).name
        assignment_list = models.Assignments.objects.filter(module_id=module_id)
        data = []
        n=0
        for name in assignment_list:
            n = n + 1
            assignment_id = name.assignment_id
            name_assignment = name.name
            if name_assignment is None:
                name_assignment = 'Assessment'
            print(name_assignment)
            request.session[str(n) + ".Assignment"] = assignment_id
            data.append(str(n) + ".Assignment")
            print(data)
    return render(request, "moduleinfo_edit.html", {"uname":uname,"credits":credits,"departments":department,"duration":duration,"students":students,"modelcode":model_code,"data":data})


# 对module 进行储存的代码
def module_edition(request):
        realname= request.POST.get("uName",None)
        module_code = request.POST.get("mCode", None)
        academic_id = models.Academics.objects.get(name=realname).academic_id
        department = request.POST.get("department", None)
        duration = request.POST.get("duration", None)
        students = request.POST.get("sNumber", None)
        credits = request.POST.get("credit", None)
        level = request.POST.get("Lever", None)
        if len(models.Modules.objects.filter(module_code=module_code))>0:
            models.Modules.objects.filter(module_code=module_code).delete()
            models.Modules.objects.create(module_id=module_code,module_code=module_code, academic_id=academic_id, department=department,
                                          duration=duration, students=students, credits=credits, level=level)
        else:
            models.Modules.objects.create(module_id=module_code,module_code=module_code, academic_id=academic_id, department=department,
                                          duration=duration, students=students, credits=credits,level=level)

        model_list = models.Modules.objects.filter(academic_id=academic_id)
        data = []
        for name in model_list:
            data.append(name.module_code)
        return render(request, "mainpart.html", {"data": data, "name": realname})





# def modulelist(request):
#     academic_id = request.POST.get("academic_id", None)
#     if len(models.Administrators.objects.filter(module_code=academic_id)) > 0:
#         return render(request, "modulelist.html",{"modellist":models.Administrators.objects.filter(module_code=academic_id).module_code } )




def countlist(request):
    if request.method == "POST":
        user_list = models.Administrators.objects.all()
        return render(request, "countlist.html", {"data": user_list})
#     教程里的展示账号密码


def pix_lecture(request):

    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("psw1", None)
        if len(models.Academics.objects.filter(email=email))>0:
            if (check_password(models.Academics.objects.get(email=email).encripted_pwd, password)):
            # if models.Academics.objects.get(email=email).encripted_pwd == password:

                id = models.Academics.objects.get(email=email).email
                request.session['member_id'] = id
                academic_id = models.Academics.objects.get(email=email).academic_id
                realname = models.Academics.objects.get(email=email).name
                model_list = models.Modules.objects.filter(academic_id=academic_id)
                data=[]
                for name in model_list:
                    data.append(name.module_code)
                return render(request, "main_frame.html")
            else:
                return render(request, "wrong.html",{"name":email} )
        else:
            return render(request, "donot.html",{"name":email} )
    email = request.session.get('member_id')
    academic_id = models.Academics.objects.get(email=email).academic_id
    realname = models.Academics.objects.get(email=email).name
    model_list = models.Modules.objects.filter(academic_id=academic_id)
    data = []
    for name in model_list:
        data.append(name.module_code)
    # return render(request, "main_frame.html", {"data": data, "name": realname})
    return render(request, "main_frame.html")



def load_lecture(request):
    email = request.session.get('member_id')
    academic_id = models.Academics.objects.get(email=email).academic_id
    realname = models.Academics.objects.get(email=email).name
    model_list = models.Modules.objects.filter(academic_id=academic_id)
    data = []
    for name in model_list:
        data.append(name.module_code)
        request.session[name.module_code] = name.module_id

    return render(request, "mainpart.html", {"data": data, "name": realname})

def load_admin(request):
    email = request.session.get('member_id')
    id = models.Administrators.objects.get(email=email).admin_id
    realname = models.Administrators.objects.get(email=email).name
    position = models.Administrators.objects.get(email=email).position
    pos = position.split(" ")
    if len(pos) == 3:
        position = pos[1]
        models_list = models.Modules.objects.filter(level=position)
    else:
        models_list = models.Modules.objects.all()
    data_control = []
    for mldule in models_list:
        module_code = mldule.module_code
        # lecturer_name = models.Academics.objects.get(academic_id=academic_id).name
        data_control.append(module_code)

    allaca_list = models.Academics.objects.all()
    control_select = []
    for name in allaca_list:
        name = name.name
        control_select.append(name)

    return render(request, "welcome.html", {"name":realname,"data_control":data_control,"data_all":control_select})


def pix_admin(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("psw1", None)
        if len(models.Administrators.objects.filter(email=email))>0:
            if(check_password(models.Administrators.objects.get(email=email).encripted_pwd,password)):
            # if models.Administrators.objects.get(email=email).encripted_pwd == password:
                realname = models.Administrators.objects.get(email=email).name
                request.session['member_id'] = email
                id = models.Administrators.objects.get(email=email).admin_id

                name_list = models.AcAd.objects.filter(admin_id=id)
                data_control = []
                for name in name_list:
                    academic_id=name.academic_id
                    lecturer_name = models.Academics.objects.get(academic_id=academic_id).name
                    data_control.append(lecturer_name)

                allaca_list = models.Academics.objects.all()
                control_select = []
                for name in allaca_list:
                    name = name.name
                    control_select.append(name)

                allmodules = models.Modules.objects.all()
                modules_select = []
                for name in allmodules:
                    module = name.module_code
                    modules_select.append(module)


                return render(request,"main_frame_admin.html",{"name":realname,"data_control":data_control,"data_all":control_select,"modules":modules_select}, )
            else:
                return render(request, "wrong.html",{"name":email} )
        else:
            return render(request, "donot.html",{"name":email} )
    email = request.session.get('member_id')
    realname = models.Administrators.objects.get(email=email).name
    return render(request,"main_frame_admin.html")


def mainpart(request):
    if request.method == "POST":
        # name = request.POST.get("add Module")
        # academic_id = request.POST.get("name")
        # return render(request, "moduleinfo.html",{"id":academic_id})
        email = request.session.get('member_id')
        name = models.Academics.objects.get(email=email).name
        return render(request, "moduleinfo.html",{"name":name})
def cancle(request):
    if request.method == "POST":
        model_id = request.POST.get("deleteModule")
        id = models.Modules.objects.get(module_code=model_id).academic_id
        models.Modules.objects.filter(module_code=model_id).delete()
        model_list = models.Modules.objects.filter(academic_id=id)
        data = []
        for name in model_list:
            data.append(name.module_code)
        username = models.Academics.objects.get(academic_id=id).name
        return render(request, "mainpart.html", {"data": data, "name": username})
def moduleinfo(request):
    pass

def assignmentinfo(request):
    pass



def clean(request):
    if request.method == "POST":
        models.Administrators.objects.create(user="", pwd="")
        # models.UserInfor.objects.

    user_list = models.Administrators.objects.all()
    return render(request, "index.html", {"data": user_list})

def welcome(request):

    return render(request, "welcome.html",)

def signin(request):
    return render(request, "signin.html",)


def signin_1(request):
    return render(request, "signin_1.html",)

def signup(request):
    return render(request, "signup.html",)

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request,"index.html")


def assignment(request):

    if request.method == "POST":
        count = 0
        # modulecode = request.POST.get("mCode", None)
        email = request.session.get('member_id')
        modulecode = request.session.get('moduleid')
        modulecturer= models.Academics.objects.get(email=email).name
        print("first",modulecturer)
        if len(models.Modules.objects.filter(module_code=modulecode))>0:
            count = len(models.Assignments.objects.filter(module_id=modulecode))+1
        moduleid = modulecode +"_"+ str(count)
        return render(request,"assignmentinfo.html",{"modulecturer": modulecturer,"moduleid":moduleid,"modulecode":modulecode})


def addassignment(request):
    if request.method == "POST":
        module_id = request.POST.get("mCode", None)
        email = request.session.get('member_id')
        acaid = models.Academics.objects.get(email=email).academic_id
        duration = models.Modules.objects.get(module_code=module_id).duration
        # name_1 = request.session.get('name')
        email = request.session.get('member_id')
        name = models.Academics.objects.get(email=email).name
        uname = name
        print("second",name)

        academic_id = models.Academics.objects.get(email=email).academic_id
        # registration_date = request.POST.get("registration_date", None)
        realease_date = request.POST.get("realease_date", None)
        realease_date= realease_date+" 00:00:00.693055+00:00"

        submission_date = request.POST.get("Submission_date", None)
        assignment_name = request.POST.get("aId", None)
        # assignment_name = assignment_name.split(".")[-1] if assignment_name is not None else None
        submission_date = submission_date+" 00:00:00.693055+00:00"
        percentage = request.POST.get("aPer", None)
        assignment_format = request.POST.get("aformat", None)
        cw_marks_format = request.POST.get("Lever", None)
        registration_date = timezone.now()
        print(type(registration_date))
        print(realease_date,registration_date)
        assignment_id = hash_text(assignment_name+str(random.randint(1,100)))
        # Validation
        with connection.cursor() as cursor:
            cursor.execute(
                "select sum(percentage) from Assignments where module_id=%s;",
                [hash_text(module_id+acaid+duration)])
            res = cursor.fetchall()
        sum = float([x[0] for x in list(res)][0] )+float(percentage)
        print("sumsumsumsumcreate",sum)
        text =''
        if sum>100:
            text += 'Percentage greater than 100%:  '+ str(sum) +" "
        sdate = parser.parse(submission_date)
        if (sdate> datetime(2018,12,1).astimezone(pytz.utc) and sdate< datetime(2018,12,31).astimezone(pytz.utc)) or sdate> datetime(2019,5,1).astimezone(pytz.utc) and sdate< datetime(2019,5,31).astimezone(pytz.utc):
            if assignment_format != "Formal exam":
                text += 'Submission date is between the exam period. '
        if sdate.weekday()>4:
            text += 'Submission data is in the weekend. '
        # dissertion is submitted in September
        if sdate<datetime(2018,9,16).astimezone(pytz.utc) or sdate>datetime(2019,9,15).astimezone(pytz.utc):
            text += 'Submission data is not within academic year. '
        if (duration == 'semester 1' and  sdate > datetime(2019,2,1).astimezone(pytz.utc))  or duration == 'semester 2' and  sdate < datetime(2019,2,1).astimezone(pytz.utc):
            text += 'Submission date is not within the corresponding semester. '
        if sdate < parser.parse(realease_date):
            text += 'Submission date should come after the release date. '

        if text == "":
            models.Assignments.objects.update_or_create(assignment_id=assignment_id, module_id=hash_text(module_id+acaid+duration), academic_id=academic_id,
                                          registration_date=registration_date,submission_date=submission_date,duration = duration,
                                          assignment_format=assignment_format, name=assignment_name, percentage=percentage, realease_date=realease_date,
                                         cw_marks_format=cw_marks_format,)
            credits = models.Modules.objects.get(module_code=module_id).credits
            department = models.Modules.objects.get(module_code=module_id).department

            students = models.Modules.objects.get(module_code=module_id).students
            assignment_list = models.Assignments.objects.filter(module_id=hash_text(module_id+acaid+duration))
            n=0
            data = []
            for name in assignment_list:
                n = n + 1
                assignment_id = name.assignment_id
                name_assignment = name.name
                if name_assignment is None:
                    name_assignment = 'Assessment'
                print(name_assignment)
                request.session[str(n) + ".Assignment"] = assignment_id
                data.append(str(n) + ".Assignment")

            return render(request, "moduleinfo_edit.html", {"uname":uname,"credits":credits,"departments":department,"duration":duration,"students":students,"modelcode":module_id,"data":data})
        else:
            return render(request, "add_assignment_error.html",{"data":text})
    # if request.method == "POST":

def addassignment_edit(request):
    if request.method == "POST":
        assignmentname = request.POST.get("name")
        module_id = request.POST.get("mCode", None)
        moduleid = request.session.get(module_id)
        print("yihhhhhhhhhhhhhhh",module_id)
        email = request.session.get('member_id')
        acaid = models.Academics.objects.get(email=email).academic_id
        duration = models.Modules.objects.get(module_code=module_id).duration
        uname = models.Academics.objects.get(email=email).name

        academic_id = models.Academics.objects.get(email=email).academic_id
        # registration_date = request.POST.get("registration_date", None)
        realease_date = request.POST.get("realease_date", None)
        realease_date= realease_date+" 00:00:00.693055+00:00"

        submission_date = request.POST.get("Submission_date", None)
        assignment_name = request.POST.get("aId", None)

        assignment_name = assignment_name.split(".")[-1] if assignment_name is not None else None
        submission_date = submission_date+" 00:00:00.693055+00:00"
        percentage = request.POST.get("aPer", None)
        assignment_format = request.POST.get("aformat", None)
        cw_marks_format = request.POST.get("Lever", None)
        registration_date = timezone.now()
        print(type(registration_date))
        print(realease_date,registration_date)
        # assignment_id = hash_text(assignment_name+str(random.randint(1,100)))
        assignment_id = request.session.get("nowassignmentid")

        request.session["now_assignment"] = assignment_id
        # request.session["assignment" + str(n)] = assignment_id
        # assignment_id = models.Assignments.objects.get(module_code=module_id).duration
        # Validation
        department = models.Modules.objects.get(module_code=module_id).department
        students = models.Modules.objects.get(module_code=module_id).students
        credits = models.Modules.objects.get(module_code=module_id).credits
        request.session["now_credits"] = credits
        request.session["now_department"] = department
        request.session["now_duration"] = duration
        request.session["now_students"] = students
        request.session["now_module_id"] = module_id
        with connection.cursor() as cursor:
            cursor.execute(
                "select sum(percentage) from Assignments where module_id=%s;",
                [hash_text(module_id+acaid+duration)])
            res = cursor.fetchall()
        sum = [x[0] for x in list(res)][0]
        old_percentage = models.Assignments.objects.get(assignment_id=assignment_id).percentage
        sum = sum - float(old_percentage) + float(percentage)
        print("sumsumsumsumedit", sum)
        text =""
        if sum>100:
            text += 'Percentage greater than 100%:  ' + str(sum) + " "
        sdate = parser.parse(submission_date)
        if (sdate> datetime(2018,12,1).astimezone(pytz.utc) and sdate< datetime(2018,12,31).astimezone(pytz.utc)) or sdate> datetime(2019,5,1).astimezone(pytz.utc) and sdate< datetime(2019,5,31).astimezone(pytz.utc):
            if assignment_format != "Formal exam":
                text += 'Submission date is between the exam period. '
        if sdate.weekday()>4:
            text += 'Submission data is in the weekend. '
        # dissertion is submitted in September
        if sdate<datetime(2018,9,16).astimezone(pytz.utc) or sdate>datetime(2019,9,15).astimezone(pytz.utc):
            text += 'Submission data is not within academic year. '
        if (duration == 'semester 1' and  sdate > datetime(2019,2,1).astimezone(pytz.utc))  or duration == 'semester 2' and  sdate < datetime(2019,2,1).astimezone(pytz.utc):
            text += 'Submission date is not within the corresponding semester. '
        if sdate < parser.parse(realease_date):
            text += 'Submission date should come after the release date. '

        if text == "":
            models.Assignments.objects.filter(assignment_id=assignment_id).delete()
            print("here")
            models.Assignments.objects.create(assignment_id=assignment_id, module_id=hash_text(module_id+acaid+duration), academic_id=academic_id,
                                          registration_date=registration_date,submission_date=submission_date,duration = duration,
                                          assignment_format=assignment_format, name=assignmentname, percentage=percentage, realease_date=realease_date,
                                         cw_marks_format=cw_marks_format,)
            credits = models.Modules.objects.get(module_code=module_id).credits
            department = models.Modules.objects.get(module_code=module_id).department

            students = models.Modules.objects.get(module_code=module_id).students
            assignment_list = models.Assignments.objects.filter(module_id=hash_text(module_id+acaid+duration))
            n=0
            data = []
            for name in assignment_list:
                n = n + 1
                assignment_id = name.assignment_id
                name_assignment = name.name
                if name_assignment is None:
                    name_assignment = 'Assessment'
                print(name_assignment)
                request.session[str(n) + ".Assignment"] = assignment_id
                data.append(str(n) + ".Assignment")


            return render(request, "moduleinfo_edit.html", {"uname":uname,"credits":credits,"departments":department,"duration":duration,"students":students,"modelcode":module_id,"data":data})
        else:
            return render(request, "add_assignment_error.html",{"data":text})

def delete_assignment(request):
    assignment_id = request.session.get("nowassignmentid")
    print("assignment_id",assignment_id)
    models.Assignments.objects.filter(assignment_id=assignment_id).delete()
    email = request.session.get('member_id')
    print("email",email)
    uname = models.Academics.objects.get(email=email).name
    credits = request.session.get('now_credits')
    department = request.session.get('now_department')
    duration = request.session.get('now_duration')
    students = request.session.get('now_students')
    module_id = request.session.get('now_module_id')
    acaid = models.Academics.objects.get(email=email).academic_id

    assignment_list = models.Assignments.objects.filter(module_id=hash_text(module_id + acaid + duration))
    n = 0
    data = []
    for name in assignment_list:
        n = n + 1
        assignment_id = name.assignment_id
        name_assignment = name.name
        if name_assignment is None:
            name_assignment = 'Assessment'
        print(name_assignment)
        request.session[str(n)+".Assignment"] = assignment_id
        data.append(str(n)+".Assignment")

    return render(request, "moduleinfo_edit.html",
                  {"uname": uname, "credits": credits, "departments": department, "duration": duration,
                   "students": students, "modelcode": module_id, "data": data})
# 下面这个用来写assignment 修改
# def addassignment_1(request):
#     if request.method == "POST":
#         name_1 = request.session.get('name')
#         email = request.session.get('member_id')
#         name = models.Academics.objects.get(email=email).name
#         module_code = request.POST.get("mCode", None)
#
#         email = request.session.get('member_id')
#         acaid = models.Academics.objects.get(email=email).academic_id
#         module_id = models.Modules.objects.get(module_code=module_code,academic_id = acaid).module_id
#         credits = models.Modules.objects.get(module_id=module_id).credits
#         department = models.Modules.objects.get(module_id=module_id).department
#         duration = models.Modules.objects.get(module_id=module_id).duration
#         students = models.Modules.objects.get(module_id=module_id).students
#         assignment_list = models.Assignments.objects.filter(module_id=hash_text(module_code + acaid + duration))
#
#
#         module_id = hash_text(module_code + acaid + duration)
#         academic_id = models.Academics.objects.get(email=email).academic_id
#         registration_date = request.POST.get("registration_date", None)
#         realease_date = request.POST.get("realease_date", None)
#         submission_date = request.POST.get("Submission_date", None)
#         percentage = request.POST.get("aPer", None)
#         assignment_format = request.POST.get("aformat", None)
#         cw_marks_format = request.POST.get("aMark", None)
#         assignment_id = request.session.get(name_1)
#         t=models.Modules.objects.get(module_id=module_id)
#         t.registration_date=registration_date
#         t.submission_date=submission_date
#         t.assignment_format=assignment_format
#         t.name=name
#         t.percentage=percentage
#         t.realease_date=realease_date
#         t.cw_marks_format=cw_marks_format
#         t.save()
#         # models.Assignments.objects.update_or_create(assignment_id=assignment_id, module_id=module_id, academic_id=academic_id,
#         #                                   registration_date=registration_date,submission_date=submission_date,
#         #                                   assignment_format=assignment_format, name=name, percentage=percentage, realease_date=realease_date,
#         #                                  cw_marks_format=cw_marks_format,)
#         n=0
#         data = []
#         for name in assignment_list:
#             n=n+1
#             assignment_id = name.assignment_id
#             request.session["assignment"+str(n)] = assignment_id
#             data.append("assignment"+str(n))
#
#         return render(request, "moduleinfo_edit.html", {"uname":name,"credits":credits,"departments":department,"duration":duration,"students":students,"modelcode":module_id,"data":data})

def assignment_edit(request):
    if request.method == "POST":

        asd = request.POST.get('submit', None)
        assignment_id = request.session.get(asd)
        asd = models.Assignments.objects.get(assignment_id=assignment_id).name
        request.session['nowassignmentid'] = assignment_id
        module_id = models.Assignments.objects.get(assignment_id=assignment_id).module_id
        modulecode = models.Modules.objects.get(module_id=module_id).module_code
        academic_id = models.Modules.objects.get(module_id=module_id).academic_id
        modulecturer = models.Academics.objects.get(academic_id=academic_id).name
        registration_date = str(models.Assignments.objects.get(assignment_id=assignment_id).registration_date)
        realease_date = str(models.Assignments.objects.get(assignment_id=assignment_id).realease_date)
        Submission_date = str(models.Assignments.objects.get(assignment_id=assignment_id).submission_date)
        aformat = models.Assignments.objects.get(assignment_id=assignment_id).assignment_format
        aPer = models.Assignments.objects.get(assignment_id=assignment_id).percentage
        return render(request,"assignmentinfo_edit.html",{"modulecode":modulecode,"modulecturer":modulecturer,"registration_date":registration_date,"realease_date":realease_date,"Submission_date":Submission_date,"aformat":aformat,"aPer":aPer,"modulename":asd})


def control_select(request):
    if request.method == "POST":
        lecturer_name = request.POST.get('selectacademic', None)
        email = request.session.get('member_id')
        admin_id = models.Administrators.objects.get(email=email).admin_id
        academic_id = models.Academics.objects.get(name=lecturer_name).academic_id

        if len(models.AcAd.objects.filter(admin_id=admin_id,academic_id=academic_id)) > 0:
            realname = models.Administrators.objects.get(email=email).name
            data_control = []
            name_list = models.AcAd.objects.filter(admin_id=admin_id)
            for name in name_list:
                academic_id = name.academic_id
                lecturer_name = models.Academics.objects.get(academic_id=academic_id).name
                data_control.append(lecturer_name)

            allaca_list = models.Academics.objects.all()
            control_select = []
            for name in allaca_list:
                name = name.name
                control_select.append(name)
            return render(request, "welcome.html",
                          {"name": realname, "data_control": data_control, "data_all": control_select})

        models.AcAd.objects.create(admin_id=admin_id,academic_id=academic_id)
        realname = models.Administrators.objects.get(email=email).name
        data_control = []
        name_list = models.AcAd.objects.filter(admin_id=admin_id)
        for name in name_list:
            academic_id = name.academic_id
            lecturer_name = models.Academics.objects.get(academic_id=academic_id).name
            data_control.append(lecturer_name)

        allaca_list = models.Academics.objects.all()
        control_select = []
        for name in allaca_list:
            name = name.name
            control_select.append(name)
        return render(request, "welcome.html",{"name": realname, "data_control": data_control, "data_all": control_select})



def report(request):
    module_code = request.session.get('module_code')

    # module_code = request.POST.get('submit', None)
    # module_code = "COM6509" # ML
    html = rep.generate_report(module_code)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)



def showassignment(request):
    module_code = request.POST.get('code', None)
    request.session['module_code'] = module_code
    with connection.cursor() as cursor:
        cursor.execute(
            "select ass.name from Assignments as ass, Modules as m where m.module_code=%s and m.module_id=ass.module_id",
            [module_code])

        res = cursor.fetchall()

    q = [x[0] for x in list(res)]
    print('here',q)
    return render(request,"showassignments.html",{"data":q,"module_code":module_code})


def filter_search(request):
    start_time = request.POST.getlist('start_time')[0]
    print("data",start_time)
    end_time = request.POST.getlist('end_time')[0]
    print("end data",end_time)
    type = request.POST.getlist('format')
    print('type',type)
    level = request.POST.getlist('level')
    print('level',level)
    modules = request.POST.getlist('modules')
    print("modules",modules)
    # request.session['start_time'] = start_time
    # request.session['end_time'] = end_time
    # request.session['fliter_format'] = format
    # request.session['filter_level'] = level
    # start_date, end_date = "01/01/2008", "12/31/2019"
    # start_date, end_date = "2018-01-01 00:00:00", "2019-12-31 23:59:00"
    hscript, hdiv,tscript,tdiv = ch.generate_charts(start_time,end_time,assig_format = type,levels = level,modules = modules)

    allmodules = models.Modules.objects.all()
    modules_select = []
    for name in allmodules:
        module = name.module_code
        modules_select.append(module)

    return render(request,"charts.html",{"hscript":hscript,"hdiv":hdiv,"tscript":tscript,"tdiv":tdiv,"modules":modules_select})



    # check_box_list = request.POST.getlist('check_box_list')

 # email = request.session.get('member_id')

def charts(request):
    start_date, end_date = "2018-01-01 00:00:00", "2019-12-31 23:59:00"
    hscript, hdiv, tscript, tdiv = ch.generate_charts(start_date, end_date)#, levels=["PGT", "4"], assig_format=["Assignment"])  # , modules = ['COM6014','COM6012',' COM4525'])
    allmodules = models.Modules.objects.all()
    modules_select = []
    for name in allmodules:
        module = name.module_code
        modules_select.append(module)
    return render(request, "charts.html", {"hscript": hscript, "hdiv": hdiv, "tscript": tscript, "tdiv": tdiv,"modules":modules_select})


def charts_academic(request):
    start_date, end_date = "2018-01-01 00:00:00", "2019-12-31 23:59:00"
    hscript, hdiv, tscript, tdiv = ch.generate_charts(start_date, end_date, levels=["PGT", "4"], assig_format=["Assignment"])  # , modules = ['COM6014','COM6012',' COM4525'])
    return render(request, "charts_academic.html", {"hscript": hscript, "hdiv": hdiv, "tscript": tscript, "tdiv": tdiv})

#
# def charts(request):
#     start_date, end_date = "01/01/2008", "12/31/2019"
#     hscript, hdiv,tscript,tdiv = ch.generate_charts(start_date,end_date)#assig_type = [type])#modules = ["COM1003", "COM4502","COM6009"])  #,levels = ["PGT"])
#     return render(request,"charts.html",{"hscript":hscript,"hdiv":hdiv,"tscript":tscript,"tdiv":tdiv})
#
# def charts_1(request):
#     start_date = request.session.get('start_time')
#     end_date = request.session.get('end_time')
#     type = request.session.get('format')
#     modules = request.session.get('modules')
#     levels = request.session.get('level')
#     # return render(request,"test.html",{"data":start_date})
#
#     # start_date, end_date = "01/01/2008", "12/31/2019"
#     hscript, hdiv,tscript,tdiv = ch.generate_charts(start_date,end_date,assig_format = type,levels = levels,modules = modules)
#     return render(request,"charts.html",{"hscript":hscript,"hdiv":hdiv,"tscript":tscript,"tdiv":tdiv})


def query_emails(request):
    start_date = request.session.get('startdata')
    end_date = request.session.get('endtime')
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, email from Academics WHERE name NOT IN ( select distinct ac.name from Assignments as ass, Academics as ac where registration_date between %s and %s and ac.academic_id=ass.academic_id)", [start_date,end_date])
        res = list(cursor.fetchall())
        res = [name + " " + email for name, email in res]
    return render(request,"showemail.html",{"data":res})