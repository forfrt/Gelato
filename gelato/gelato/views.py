import json
import random
import string

from gelato import models
from gelato.forms import *
from django.views import View
from django.template import loader
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic.edit import FormView
from django.core.mail import EmailMultiAlternatives

user_list = [
    {"user":"jack","pwd":"abc"},
    {"user":"wom","pwd":"ABC"},
]

FROM_EMAIL='rtfeng12@gamil.com'

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

    return render(request, "registration.html", {"note": ""})

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
        module_deleted=models.Modules.objects.filter(module_code=module_code)
        module_deleted.delete()
        return json.dumps(request_dict)


def moduleinfo_edit(request):
    if request.method == "POST":
        model_code=request.POST.get("submit",None)
        request.session['moduleid'] = model_code
        credits = models.Modules.objects.get(module_code=model_code).credits
        department = models.Modules.objects.get(module_code=model_code).department
        duration = models.Modules.objects.get(module_code=model_code).duration
        students = models.Modules.objects.get(module_code=model_code).students
        id = models.Modules.objects.get(module_code=model_code).academic_id
        name = models.Academics.objects.get(academic_id=id).name
        module_id = models.Modules.objects.get(module_code=model_code).module_id
        assignment_list = models.Assignments.objects.filter(module_id=module_id)
        data = []
        for name in assignment_list:
            data.append(name.assignment_id)
    return render(request, "moduleinfo_edit.html", {"uname":name,"credits":credits,"departments":department,"duration":duration,"students":students,"modelcode":model_code,"data":data})


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


def login(request):
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

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

def assignment(request):

    if request.method == "POST":
        count = 0
        email = request.session.get('member_id')
        modulecode = request.session.get('moduleid')
        modulecturer= models.Academics.objects.get(email=email).name
        if len(models.Modules.objects.filter(module_code=modulecode))>0:
            count = len(models.Assignments.objects.filter(module_id=modulecode))+1
        moduleid = modulecode +"_"+ str(count)
        return render(request,"assignmentinfo.html",{"modulecturer": modulecturer,"moduleid":moduleid,"modulecode":modulecode})


def addassignment(request):
    if request.method == "POST":
        email = request.session.get('member_id')
        name = models.Academics.objects.get(email=email).name
        module_id = request.POST.get("mCode", None)
        assignment_id = request.POST.get("aId", None)
        academic_id = models.Academics.objects.get(email=email).academic_id
        registration_date = request.POST.get("registration_date", None)
        realease_date = request.POST.get("realease_date", None)
        submission_date = request.POST.get("Submission_date", None)
        percentage = request.POST.get("aPer", None)
        assignment_format = request.POST.get("aformat", None)
        cw_marks_format = request.POST.get("aMark", None)
        models.Assignments.objects.create(assignment_id=assignment_id, module_id=module_id, academic_id=academic_id,
                                          registration_date=registration_date,submission_date=submission_date,
                                          assignment_format=assignment_format, name=name, percentage=percentage, realease_date=realease_date,
                                         cw_marks_format=cw_marks_format,)
        credits = models.Modules.objects.get(module_code=module_id).credits
        department = models.Modules.objects.get(module_code=module_id).department
        duration = models.Modules.objects.get(module_code=module_id).duration
        students = models.Modules.objects.get(module_code=module_id).students
        assignment_list = models.Assignments.objects.filter(module_id=module_id)
        data = []
        for name in assignment_list:
            data.append(name.assignment_id)
        return render(request, "moduleinfo_edit.html", {"uname":name,"credits":credits,"departments":department,"duration":duration,"students":students,"modelcode":module_id,"data":data})
    # if request.method == "POST":



def assignment_edit(request):
    if request.method == "POST":
        assignment_id = request.POST.get('submit', None)
        modulecode = models.Assignments.objects.get(assignment_id=assignment_id).module_id
        modulecturer = models.Assignments.objects.get(assignment_id=assignment_id).name
        registration_date = str(models.Assignments.objects.get(assignment_id=assignment_id).registration_date)
        realease_date = str(models.Assignments.objects.get(assignment_id=assignment_id).realease_date)
        Submission_date = str(models.Assignments.objects.get(assignment_id=assignment_id).submission_date)
        aformat = models.Assignments.objects.get(assignment_id=assignment_id).assignment_format
        aPer = models.Assignments.objects.get(assignment_id=assignment_id).percentage

        return render(request,"assignmentinfo_edit.html",{"assignmentid":assignment_id,"modulecode":modulecode,"modulecturer":modulecturer,"registration_date":registration_date,"realease_date":realease_date,"Submission_date":Submission_date,"aformat":aformat,"aPer":aPer})

def send_password_email(email, password):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

# class AdminProfileView(FormView):
#     form_class=AdminProfileForm
#     template_name="admin_profile.html"
#     
#     def form_valid(self, form):
#         return super().form_valid(form)
# 
#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         return context
# 
#     def get_initial(self):
#         initial=super(AdminProfileView, self).get_initial()
#         if initial:
#             return initial
#         else:
#             if self.request.session['admin_id']:
#                 return models.Administrators.objects.get(admin_id='04db271174d438e6bed967709e73d77a').__dict__
#             else:
#                 return 

class AdminProfileView(View):
    form_class=AdminProfileForm
    template_name="admin_profile.html"

    def post(self, request, *args, **kwargs):
        #if 'admin_id' in self.request.session and self.request.session['admin_id']:
        admin_id='04db271174d438e6bed967709e73d77a'
        if True:
            admin=models.Administrators.objects.get(admin_id=admin_id)
            message=''

            form=AdminProfileForm(self.request.POST)
            if form.is_valid():
                admin.name          =form.cleaned_data['name']
                admin.email         =form.cleaned_data['email']
                admin.position      =form.cleaned_data['position']
                admin.encripted_pwd =form.cleaned_data['encripted_pwd']
                admin.save()

                ac_ad_set=models.AcAd.objects.filter(admin__admin_id=admin.admin_id)
                acades=list()
                for ac_ad in ac_ad_set:
                    acade=models.Academics.objects.get(academic_id=ac_ad.academic_id)
                    acades.append(acade)

                message='Update Successfully'
            else:
                message='Update failed'

            return render(request, 'admin_profile.html', {'form':form, 'acades': acades, 'message':message})
        else:
            return render(request, 'session_missed.html')

    def get(self, request, *args, **kwargs):
        #if 'admin_id' in self.request.session and self.request.session['admin_id']:
        if True:
            admin=models.Administrators.objects.get(admin_id='04db271174d438e6bed967709e73d77a')
            form=AdminProfileForm(admin.__dict__)
            ac_ad_set=models.AcAd.objects.filter(admin__admin_id=admin.admin_id)
            acades=list()
            for ac_ad in ac_ad_set:
                acade=models.Academics.objects.get(academic_id=ac_ad.academic_id)
                acades.append(acade)

            return render(request, 'admin_profile.html', {'form':form, 'acades': acades})
        else:
            return render(request, 'session_missed.html')


class AcadeProfileView(View):
    form_class=AcadeProfileForm
    template_name="acade_profile.html"

    def post(self, request, *args, **kwargs):
        # if 'admin_id' in self.request.session and self.request.session['admin_id']:
        acade_id='cffa0015f8ce5f48646929c5a8d6ae15'
        if True:
            acade=models.Academics.objects.get(academic_id=acade_id)
            message=''

            form=AcadeProfileForm(request.POST)
            if form.is_valid():
                acade.name          =form.cleaned_data['name']
                acade.email         =form.cleaned_data['email']
                acade.encripted_pwd =form.cleaned_data['encripted_pwd']
                acade.save()
                message='Update Successfully'
            else:
                message='Update failed'

            return render(request, 'acade_profile.html', {'form':form, 'message':message})
        else:
            return render(request, 'session_missed.html')

    def get(self, request, *args, **kwargs):
        # if 'admin_id' in self.request.session and self.request.session['admin_id']:
        acade_id='cffa0015f8ce5f48646929c5a8d6ae15'
        if True:
            acade=models.Academics.objects.get(academic_id=acade_id)
            form=AcadeProfileForm(acade.__dict__)

            return render(request, 'acade_profile.html', {'form':form})
        else:
            return render(request, 'session_missed.html')

PASSWD_LENGTH=10

class PasswdResetView(View):

    def get(self, request, *args, **kwargs):
        form=PasswdResetForm()
        return render(request, 'passwd_reset.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form=PasswdResetForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['label']=='acade':
                try:
                    acade=models.Academics.objects.get(email=form.cleaned_data['email'])
                    rand_passwd=random_passwd()
                    acade.cripted_pwd=rand_passwd
                    acade.save()

                    subject, from_email, to = 'Password_Reset', FROM_EMAIL, 'forfrt@gmail.com'
                    text_content = 'Your new password is {}'.format(rand_passwd)
                    html_content = '<p>Your new password is <strong>{{pwd}}</strong></p>'
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content.render({'pwd':rand_passwd}, requeset), "text/html")
                    msg.send()

                    return render(request, 'passwd_reset_done.html', {'email': to})

                except models.Academics.DoesNotExist:
                    message="The academics does not exist"
                    return render(request, 'passwd_reset.html', {'form': form, 'message':message})

            elif form.cleaned_data['label']=='admin':
                try:
                    admin=models.Administrators.objects.get(email=form.cleaned_data['email'])
                    rand_passwd=random_passwd()
                    admin.cripted_pwd=rand_passwd
                    admin.save()

                    subject, from_email, to = 'Password_Reset', FROM_EMAIL, admin.email
                    text_content = 'Your new password is {}'.format(rand_passwd)
                    html_content = '<p>Your new password is <strong>{{pwd}}</strong></p>'
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content.render({'pwd':rand_passwd}, requeset), "text/html")
                    msg.send()

                    return render(request, 'passwd_reset_done.html', {'email': to})

                except models.Administrators.DoesNotExist:

                    rand_passwd=random_passwd()

                    subject, from_email, to = 'Password_Reset', FROM_EMAIL, 'forfrt@gmail.com'
                    text_content = 'Your new password is {}'.format(rand_passwd)
                    html_content = loader.get_template('passwd_reset_email.html')
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content.render({'pwd':rand_passwd}, request), "text/html")
                    msg.send()

                    return render(request, 'passwd_reset_done.html', {'email': to})

                    #message="The adminisrator does not exist"
                    #return render(request, 'passwd_reset.html', {'form': form, 'message':message})
        else:
            message=form.cleaned_data
            return render(request, 'passwd_reset.html', {'form': form, 'message':message})


def random_passwd(length=PASSWD_LENGTH):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

