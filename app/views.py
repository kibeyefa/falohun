from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages import add_message, error, success
# from django.contrib.auth.password_validation  import valida
from django.contrib.auth.hashers import make_password, check_password

from app.models import *

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('/doctor/dashboard/')
        else:
            return redirect('student/dashboard/')
       
    return redirect("/student/login/")


class LogoutView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            logout(request)

        return redirect("/")


class StudentLoginView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/student/dashboard/')
        
        return render(request, 'student/login.html')
    
    def post(self, request):
        matric_number, password = self.request.POST.get('matric_no'), self.request.POST.get('password')
        try:
            profile = StudentProfile.objects.get(matric_number=matric_number)
            email = profile.student.email
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/student/dashboard/')
            else:
                error(request, "Ivalid Matric Number or Password")
        except:
            error(request, "Ivalid Matric Number or Password")
        
        return render(request, 'student/login.html') 


class StudentRegisterView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/student/dashboard/')
        
        return render(request, 'student/register.html')


class StudentDashboardView(View):
    def get(self, request):
        if not self.request.user.is_authenticated or not self.request.user.is_student:
            return redirect('/student/login/')
        user = self.request.user
        profile = StudentProfile.objects.get_or_create(student=user)
        profile = profile[0]
        appointments = Appointment.objects.filter(student=profile)
        context = dict(profile=profile, appointments=appointments)
        
        return render(request, 'student/dashboard-index.html', context)


class StudentAppointmentView(View):
    def get(self, request):
        if not self.request.user.is_authenticated or not self.request.user.is_student:
            return redirect('/student/login/')
        user = request.user
        profile = StudentProfile.objects.get_or_create(student=user)
        profile = profile[0]
        appointments = Appointment.objects.filter(student=profile)
        doctors = DoctorProfile.objects.all()
        context = dict(profile=profile, appointments=appointments, doctors=doctors)
        return render(request, 'student/appointments.html', context)
    
    def post(self, request):
        user = request.user
        profile = StudentProfile.objects.get_or_create(student=user)
        profile = profile[0]
        doctor = DoctorProfile.objects.get(id=self.request.POST.get('doctor'))
        try:
            appointment = Appointment.objects.create(student=profile, doctor=doctor, appointe_date=self.request.POST.get('date'), 
                                                    start_time=self.request.POST.get('start_time'), end_time=self.request.POST.get('end_time'))
            success(request, "Appointment created successfully")
        except:
            error(request, "An error occured")
        return redirect("/student/appointments/")


class StudentProfileView(View):
    def get(self, request):
        user = self.request.user
        if not user.is_authenticated or not user.is_student:
            return redirect('/student/login/')     

        profile = StudentProfile.objects.get(student=user) 
        return render(request, 'student/profile.html', {'profile': profile})
    
    def post(self, request):
        user = self.request.user
        if not user.is_authenticated or not user.is_student:
            return redirect('/student/login/')
        
        profile = StudentProfile.objects.get(student=user)         
        if user.check_password(self.request.POST.get('old_password')):
            print('correct password')
            user.set_password(self.request.POST.get('new_password'))
            success_msg = "Password Changed Succesfully"
            feedback = False
        else:
            feedback = "Incorrect Password"
            success_msg = False
            
        print(feedback)    
        return render(request, 'student/profile.html', {'profile': profile, "feedback": feedback, "success_msg": success_msg})
      

class StudentAppointmentCancelView(View):
    def get(self, request, appointment_id):
        apppointment = Appointment.objects.get(id=appointment_id)
        apppointment.status = 'canceled'
        apppointment.save()
        return redirect("/student/appointments/")


class StudentAppointmentDeleteView(View):
    def get(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.delete()
        return redirect("/student/appointments/")


class StudentTestResultsView(View):
    def get(self, request):
        user = self.request.user
        if not user.is_authenticated or not user.is_student:
            return redirect('/student/login/')
        
        profile = StudentProfile.objects.get(student=user)
        test_results = TestResult.objects.filter(student=profile)
        context = dict(profile=profile, test_results=test_results)

        return render(request, 'student/test-results.html', context)      

class DoctorLoginView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/student/dashboard/')
        return render(request, 'doctor/login.html')
    
    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None and user.is_doctor:
            login(request, user)
            return redirect('/doctor/dashboard/')
        else:
            error(request, "Invalid credentials or user not a doctor")
            return redirect('/doctor/login/')


class DoctorProfileView(View):
    def get(self, request):
        user = self.request.user
        if not user.is_authenticated or not user.is_doctor:
            return redirect('/doctor/login/')     

        profile = DoctorProfile.objects.get(doctor=user) 
        return render(request, 'doctor/profile.html', {'profile': profile})
    
    def post(self, request):
        user = self.request.user
        if not user.is_authenticated or not user.is_doctor:
            return redirect('/doctor/login/')
        
        profile = DoctorProfile.objects.get(student=user)         
        if user.check_password(self.request.POST.get('old_password')):
            print('correct password')
            user.set_password(self.request.POST.get('new_password'))
            success_msg = "Password Changed Succesfully"
            feedback = False
        else:
            feedback = "Incorrect Password"
            success_msg = False
            
        print(feedback)    
        return render(request, 'doctor/profile.html', {'profile': profile, "feedback": feedback, "success_msg": success_msg})
   

class DoctorDashboardView(View):
    def get(self, request):
        if not self.request.user.is_authenticated or not self.request.user.is_doctor:
            return redirect('/doctor/login/')
        user = self.request.user
        profile = DoctorProfile.objects.get_or_create(doctor=user)
        profile = profile[0]
        appointments = Appointment.objects.filter(doctor=profile)
        context = dict(profile=profile, appointments=appointments)
        
        return render(request, 'doctor/dashboard-index.html', context)


class DoctorAppointmentView(View):
    def get(self, request):
        if not self.request.user.is_authenticated or not self.request.user.is_doctor:
            return redirect('/dcotor/login/')
        user = request.user
        profile = DoctorProfile.objects.get_or_create(doctor=user)
        profile = profile[0]
        appointments = Appointment.objects.filter(doctor=profile)
        doctors = DoctorProfile.objects.all()
        context = dict(profile=profile, appointments=appointments, doctors=doctors)
        return render(request, 'doctor/appointments.html', context)


class DoctorAppointmentApproveView(View):
    def get(self, request, appointment_id):
        apppointment = Appointment.objects.get(id=appointment_id)
        apppointment.status = 'approved'
        apppointment.save()
        return redirect("/doctor/appointments/")


class DoctorAppointmentCancelView(View):
    def get(self, request, appointment_id):
        apppointment = Appointment.objects.get(id=appointment_id)
        apppointment.status = 'canceled'
        apppointment.save()
        return redirect("/doctor/appointments/")


class DoctorStudentRecordAdditionView(View):
    def post(self, request):
        user = request.user
        matric_no = self.request.POST.get('matric-no')
        file = self.request.FILES.get('file')
        print(file)
        if StudentProfile.objects.filter(matric_number=matric_no).exists():
            test_result = TestResult.objects.create(doctor=DoctorProfile.objects.get(doctor=user), 
                                                    student=StudentProfile.objects.get(matric_number=matric_no), file=file)
        else:
            error(request, f"Student with Matric No {matric_no} does not exist.")
        return redirect("/doctor/dashboard/")
