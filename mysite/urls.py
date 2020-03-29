"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

def about(request):
    return HttpResponse('about')

urlpatterns = [
    path('',LoginView.as_view(template_name='base/login.html'), name="login"),
    path('admin/', admin.site.urls),
    path('about/', views.about),
    path('profile/', views.Profile),
    path('login/', LoginView.as_view(template_name='base/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='base/logout.html'), name="logout"),
    path('register/', views.register, name='register'),
    path('newshift/', views.newshift),
    path('managerstaffing/', views.managerstaffing),
    path('staffingshow/', views.staffingshow),
    path('myshifts/', views.myshifts),
    path('allshifts/', views.allshifts),
    path('contact/', views.contact),
    path('managercontact/', views.managercontact),
    path('managershowalljobs/', views.managershowalljobs),
    path('deletejob/',views.deletejob),
    path('unmannedshifts/', views.unmannedshifts),
    path('airgoals/', views.airgoals),
    path('airgoalsinfo/', views.airgoalsinfo),
    path('managerunmanned/', views.managerunmanned),
    path('managershifts/',views.managershifts),
    path('managergoalupdate/',views.managergoalupdate),
    path('managergoalupdateshow/',views.managergoalupdateshow),
    path('deletegoals/',views.deletegoals),
    path('deletecontact/',views.deletecontact),
    path('managerapproved/', views.managerapproved),
    path('deletestaffing/', views.deletestaffing),
    path('managermyweek/', views.managermyweek),

              ]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


