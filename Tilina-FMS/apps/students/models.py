from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import StudentClass


class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    # registration_number = models.CharField(max_length=200, unique=True)
    last_name = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    middle_name = models.CharField(max_length=60, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    village = models.CharField(max_length=60)
    traditional_authority = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    others = models.TextField(blank=True)
    address = models.TextField(blank=True, verbose_name="Residential Address")
    denomination = models.CharField(max_length=60)
    allergies = models.TextField(blank=True)
    medical_doctor = models.CharField(max_length=60)



    passport = models.ImageField(blank=True, upload_to="students/passports/")

    class Meta:
        ordering = ["last_name", "first_name", "middle_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
