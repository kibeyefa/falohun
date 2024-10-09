from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django_extensions.db.models import TimeStampedModel

from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=2000, blank=True, null=True)
    phone = models.CharField(max_length=11)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    is_student = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone"]  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)


class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE,)
    matric_number = models.CharField(max_length=255, unique=True)
    surname = models.CharField(max_length=255,)
    first_name = models.CharField(max_length=255,)
    faculty = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    level = models.CharField(choices=(("100", "100"), ("200", "200"), ("300", "300"), ("400", "400"), ("500", "500")), max_length=255)
    profile_image = models.FileField(upload_to="static/uploads", blank=True, null=True)

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def __str__(self):
        return self.surname + " " + self.first_name

    def save(self, *args, **kwargs):
        self.matric_number = self.matric_number.upper()
        return super().save(*args, **kwargs)


class DoctorProfile(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,)
    emails = models.EmailField(max_length=255,)
    phone = models.CharField(max_length=11,)
    profile_image = models.FileField(upload_to="static/uploads", blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctor Profiles'


class Appointment(TimeStampedModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, blank=True, null=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, blank=True, null=True)
    appointe_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=255, default='pending', 
                              choices=(("pending", "pending"),("canceled", "canceled"), ("approve", "approve") ))

    def __str__(self):
        return f"Appointment between {self.student.first_name} with Matric no {self.student.matric_number} and Doctor {self.doctor.name}"
    

class TestResult(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="static/uploads/test_results", blank=True, null=True)

    def __str__(self):
        return f"{self.doctor.name} - {self.student.matric_number}"