from django.shortcuts import render

# Create your views here.



from django.shortcuts import render
from django.shortcuts import HttpResponse
from gelato import models
# Create your views here.


user_list = [
    {"user":"jack","pwd":"abc"},
    {"user":"wom","pwd":"ABC"},
]




def index(request):
    # pass


    if request.method == "POST":
        return render(request, "registration.html", )



    return render(request, "index.html",)


def registration(request):

    if request.method == "POST":
        username = request.POST.get("uid", None)
        password = request.POST.get("pswl", None)
        # 添加数据到数据库
        if len(models.UserInfor.objects.filter(user=username))>0:
            return render(request, "used.html",)
        else:
            models.UserInfor.objects.create(user=username, pwd=password)
        return render(request, "registration.html", {"note": "registration complete!"})
    return render(request, "registration.html", {"note": ""})

def countlist(request):
    if request.method == "POST":
        user_list = models.UserInfor.objects.all()
        return render(request, "countlist.html", {"data": user_list})

def pix(request):
    if request.method == "POST":
        username = request.POST.get("uid", None)

        password = request.POST.get("psw1", None)
        if len(models.UserInfor.objects.filter(user=username))>0:
            if models.UserInfor.objects.get(user=username).pwd == password:
                return render(request, "welcome.html",{"name":username} )
            else:
                return render(request, "wrong.html",{"name":username} )
        else:
            return render(request, "donot.html",{"name":username} )


def clean(request):
    if request.method == "POST":
        models.UserInfor.objects.create(user="", pwd="")
        # models.UserInfor.objects.

    user_list = models.UserInfor.objects.all()
    return render(request, "index.html", {"data": user_list})

def welcome(request):

    return render(request, "welcome.html",)

def signin(request):
    return render(request, "signin.html",)

def signup(request):
    return render(request, "signup.html",)