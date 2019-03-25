"""gelato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from gelato import views


urlpatterns = [

    # path('admin/', admin.site.urls),
    path('signin/<int:role_id>', view.signin_pages)
    path('login', view.login)

    path('index/', views.index),
    path('welcome/', views.welcome),
    path('clean/', views.clean),
    path('registration/',views.registration),
    path('countlist/',views.countlist),
    path('signup/',views.signup),
    path('mainpart/',views.mainpart),
    path('moduleinfo/',views.moduleinfo),
    path('assignmentinfo/',views.assignmentinfo),
    path('moduleadd/',views.moduleadd),
    path('moduleinfo_edit/',views.moduleinfo_edit),
    path('cancle/',views.cancle),
    path('module_edition/',views.module_edition),

    # path('signin/',views.signin),
    # path('signin_1/',views.signin_1),

    # path('pix_admin/', views.pix_admin),
    # path('pix_lecture/', views.pix_lecture),
]
