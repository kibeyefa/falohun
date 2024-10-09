"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from pydoc import pager
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("", home, name=""),
    path('admin/', admin.site.urls),
    path('auth/signout/', LogoutView.as_view())
]

urlpatterns += [
    path('student/login/', StudentLoginView.as_view()),
    path('student/profile/', StudentProfileView.as_view()),
    path('student/dashboard/', StudentDashboardView.as_view()),
    path('student/test-results/', StudentTestResultsView.as_view()),
    path('student/appointments/', StudentAppointmentView.as_view()),
    path('student/appointments/cancel/<appointment_id>/', StudentAppointmentCancelView.as_view()),
    path('student/appointments/delete/<appointment_id>/', StudentAppointmentDeleteView.as_view()),
]

urlpatterns += [
    path('doctor/login/', DoctorLoginView.as_view()),
    path('doctor/profile/', DoctorProfileView.as_view()),
    path('doctor/dashboard/', DoctorDashboardView.as_view()),
    path('doctor/appointments/', DoctorAppointmentView.as_view()),
    path('doctor/appointments/cancel/<appointment_id>/', DoctorAppointmentCancelView.as_view()),
    path('doctor/appointments/approve/<appointment_id>/', DoctorAppointmentApproveView.as_view()),
    path('doctor/test-result/add/', DoctorStudentRecordAdditionView.as_view()),
]
