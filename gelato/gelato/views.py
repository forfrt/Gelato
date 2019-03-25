import json

from gelato import models
from django.shortcuts import render
from django.shortcuts import HttpResponse

user_list = [
    {"user":"jack","pwd":"abc"},
    {"user":"wom","pwd":"ABC"},
]

def index(request):

    if request.method == "POST":
        return render(request, "registration.html", )

    return render(request, "index.html",)


def registration(request):

    if request.method == "POST":
        identity = request.POST.get("identity", None)
        id = request.POST.get("id", None)
        username = request.POST.get("uid", None)
        password = request.POST.get("pswl", None)
        email = request.POST.get("email", None)
        realname = request.POST.get("realname", None)
        position = request.POST.get("pos", None)
        # 添加数据到数据库
        if identity == '0':
            if len(models.Academics.objects.filter(academic_id=id))>0:
                return render(request, "used.html",)
            elif len(models.Academics.objects.filter(uername=username))>0:
                return render(request, "used.html", )
            else:
                models.Academics.objects.create(academic_id=id,email=email,name=realname, uername=username, encripted_pwd=password)
                return render(request, "registration.html", {"note": "registration complete!"})
        elif identity== '1':
            if len(models.Administrators.objects.filter(admin_id=id))>0:
                return render(request, "used.html",)
            elif len(models.Administrators.objects.filter(uername=username))>0:
                return render(request, "used.html",)
            else:
                models.Administrators.objects.create(admin_id=id, position=position,email=email,name=realname, uername=username, encripted_pwd=password)
                return render(request, "registration.html", {"note": "registration complete!"})



def moduleadd(request):
    if request.method == "POST":
        username = request.POST.get("uName",None)
        module_code = request.POST.get("mCode", None)
        academic_id = models.Academics.objects.get(uername=username).academic_id
        department = request.POST.get("department", None)
        duration = request.POST.get("duration", None)
        students = request.POST.get("sNumber", None)
        credits = request.POST.get("credit", None)
        level = request.POST.get("Lever", None)
        if len(models.Modules.objects.filter(module_code=module_code))>0:
            return render(request, "used.html", )
        else:
            models.Modules.objects.create(module_code=module_code, academic_id=academic_id, department=department,
                                          duration=duration, students=students, credits=credits,level=level)
        model_list = models.Modules.objects.filter(academic_id=academic_id)
        data = []
        for name in model_list:
            data.append(name.module_code)
        return render(request, "mainpart.html", {"data": data, "name": username})

def module_delete(request):
    if request.method == "POST":
        request_dict=json.loads(request.POST)
        module_code=request_dict.get('module_code', None)
        module_deleted=modules.Modules.objects.filter(module_code=module_code)
        module_deleted.delete()
        return json.dumps(request_dict)



def moduleinfo_edit(request):
    if request.method == "POST":
        model_code=request.POST.get("submit",None)
        credits = models.Modules.objects.get(module_code=model_code).credits
        department = models.Modules.objects.get(module_code=model_code).department
        duration = models.Modules.objects.get(module_code=model_code).duration
        students = models.Modules.objects.get(module_code=model_code).students
        id = models.Modules.objects.get(module_code=model_code).academic_id
        uname = models.Academics.objects.get(academic_id=id).uername
    return render(request, "moduleinfo_edit.html", {"uname":uname,"credits":credits,"departments":department,"duration":duration,"students":students,"modelcode":model_code})


def module_edition(request):
    if request.method == "POST":
        username = request.POST.get("uName",None)
        module_code = request.POST.get("mCode", None)
        academic_id = models.Academics.objects.get(uername=username).academic_id
        department = request.POST.get("department", None)
        duration = request.POST.get("duration", None)
        students = request.POST.get("sNumber", None)
        credits = request.POST.get("credit", None)
        level = request.POST.get("Lever", None)
        if len(models.Modules.objects.filter(module_code=module_code))>0:
            models.Modules.objects.filter(module_code=module_code).delete()
            models.Modules.objects.create(module_code=module_code, academic_id=academic_id, department=department,
                                          duration=duration, students=students, credits=credits, level=level)
        else:
            models.Modules.objects.create(module_code=module_code, academic_id=academic_id, department=department,
                                          duration=duration, students=students, credits=credits,level=level)
        model_list = models.Modules.objects.filter(academic_id=academic_id)
        data = []
        for name in model_list:
            data.append(name.module_code)
        return render(request, "mainpart.html", {"data": data, "name": username})





# def modulelist(request):
#     academic_id = request.POST.get("academic_id", None)
#     if len(models.Administrators.objects.filter(module_code=academic_id)) > 0:
#         return render(request, "modulelist.html",{"modellist":models.Administrators.objects.filter(module_code=academic_id).module_code } )


def countlist(request):
    if request.method == "POST":
        user_list = models.Administrators.objects.all()
        return render(request, "countlist.html", {"data": user_list})
#     教程里的展示账号密码


def mainpart(request):
    if request.method == "POST":
        name = request.POST.get("add Module")
        # academic_id = request.POST.get("name")

        # return render(request, "moduleinfo.html",{"id":academic_id})
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
        username = models.Academics.objects.get(academic_id=id).uername
        return render(request, "mainpart.html", {"data": data, "name": username})
def moduleinfo(request):
    pass

def assignmentinfo(request):
    pass

def signin_pages(request, role_id):
    if request.method=="GET":
        return render(request, "sigin.html", {"role":role_id})


def login(request, role_id):
    if request.method == "POST":
        username = request.POST.get("uid", None)
        password = request.POST.get("psw", None)
        role=reqeust.POST.get("role", None)

        if role==1:
            if len(models.Administrators.objects.filter(uername=username))>0:
                if models.Administrators.objects.get(uername=username).encripted_pwd == password:
                    username = models.Administrators.objects.get(uername=username).uername
                    return render(request, "welcome.html",{"name":username} )
                else:
                    return render(request, "wrong.html",{"name":username} )
            else:
                return render(request, "donot.html",{"name":username} )
        elif role==0:
            if len(models.Academics.objects.filter(uername=username))>0:
                if models.Academics.objects.get(uername=username).encripted_pwd == password:
                    academic_id = models.Academics.objects.get(uername=username).academic_id
                    module_list = models.Modules.objects.filter(academic_id=academic_id)
                    return render(request, "mainpart.html",{"module_list":module_list})
                else:
                    return render(request, "wrong.html",{"name":username} )
            else:
                return render(request, "donot.html",{"name":username} )

        else:
            # TODO 404
            pass



def clean(request):
    if request.method == "POST":
        models.Administrators.objects.create(user="", pwd="")
        # models.UserInfor.objects.

    user_list = models.Administrators.objects.all()
    return render(request, "index.html", {"data": user_list})

def welcome(request):

    return render(request, "welcome.html",)

def signup(request):
    return render(request, "signup.html", )
