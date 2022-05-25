from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import StudentClass



class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )

    last_name = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    middle_name = models.CharField(max_length=60, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField()
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    village = models.CharField(max_length=60)
    traditional_authority = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    address = models.TextField(blank=True, verbose_name="Residential Address")
    denomination = models.CharField(max_length=60)
    allergies = models.CharField(max_length=300)
    medical_doctor_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    passport = models.ImageField(blank=True, upload_to="students/passports/")

    class Meta:
        ordering = ["last_name", "first_name", "middle_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})


class Guardian(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    RELATION_CHOICES = [("mother", "Mother"), ("father", "Father")]
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES, default="father")
    created_at = models.DateTimeField(default=timezone.now)
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    email = models.EmailField()
    occupation = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
