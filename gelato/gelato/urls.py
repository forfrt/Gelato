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
from django.urls import include, path, re_path
from gelato import views
# from django.contrib.auth import views as auth_views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('signin_<int:role_id>/', views.signin_pages),
    path('login/', views.login),

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
    path('addassignment/', views.addassignment),
    path('assignment/', views.assignment),
    path('assignment_edit/', views.assignment_edit, ),

    # path('users/password_reset/', auth_views.PasswordResetView.as_view()),
    # path('users/password_reset/done/', auth_views.PasswordResetDoneView.as_view()),
    # path('users/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view()),
    # path('users/reset/done/', auth_views.PasswordResetCompleteView.as_view()),

    path('password_reset/', views.PasswdResetView.as_view(), name="passwd_reset"),
    path('admin/profile/', views.AdminProfileView.as_view(), name="admin_profile"),
    path('acade/profile/', views.AcadeProfileView.as_view(), name="acade_profile"),
    #path('user/password_reset/', views.user_profile)
    #path('user/password_reset/', views.user_profile)
    #path('user/password_reset/', views.user_profile)
    #path('user/password_reset/', views.user_profile)
]
