import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import StudentGuardianFormset, Students
from apps.finance.models import Invoice

from .models import Student, Guardian, StudentBulkUpload


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = "students/student_list.html"


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(student=self.object)
        context["guardians"] = Guardian.objects.filter(student=self.object)

        return context


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'current_class',
              'date_of_admission', 'village', 'traditional_authority', 'district', 'address',
              'denomination', 'allergies', 'medical_doctor_number']

    success_message = "New student successfully added."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        return form

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["guardians"] = StudentGuardianFormset(
                self.request.POST, prefix="studentguardian_set"
            )
        else:
            context["guardians"] = StudentGuardianFormset(prefix="studentguardian_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["guardians"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'current_class',
              'date_of_admission', 'village', 'traditional_authority', 'district', 'address',
              'denomination', 'allergies', 'medical_doctor_number']

    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        return form

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["guardians"] = StudentGuardianFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["guardians"] = StudentGuardianFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["guardians"]
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Student
    success_message = "Student successfully Deleted."
    success_url = reverse_lazy("student-list")


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "last_name",
                "first_name",
                "middle_names",
                "gender",
                "parent_number",
                "address",
                "current_class",
            ]
        )

        return response
