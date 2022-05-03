import csv
import os
from io import StringIO

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.corecode.models import StudentClass

from .models import Student, StudentBulkUpload


@receiver(post_save, sender=StudentBulkUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=",")
        students = []
        for row in reading:
            if "registration_number" in row and row["registration_number"]:
                reg = row["registration_number"]
                last_name = row["last_name"] if "last_name" in row and row["last_name"] else ""
                first_name = (
                    row["first_name"] if "first_name" in row and row["first_name"] else ""
                )
                middle_names = (
                    row["middle_names"]
                    if "middle_names" in row and row["middle_names"]
                    else ""
                )
                gender = (
                    (row["gender"]).lower() if "gender" in row and row["gender"] else ""
                )
                phone = (
                    row["parent_number"]
                    if "parent_number" in row and row["parent_number"]
                    else ""
                )
                address = row["address"] if "address" in row and row["address"] else ""
                current_class = (
                    row["current_class"]
                    if "current_class" in row and row["current_class"]
                    else ""
                )
                if current_class:
                    theclass, kind = StudentClass.objects.get_or_create(
                        name=current_class
                    )

                check = Student.objects.filter(registration_number=reg).exists()
                if not check:
                    students.append(
                        Student(
                            registration_number=reg,
                            last_name=last_name,
                            first_name=first_name,
                            middle_name=middle_names,
                            gender=gender,
                            current_class=theclass,
                            parent_mobile_number=phone,
                            address=address,
                            current_status="active",
                        )
                    )

        Student.objects.bulk_create(students)
        instance.csv_file.close()
        instance.delete()


def _delete_file(path):
    """Deletes file from filesystem."""
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=StudentBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Student)
def delete_passport_on_delete(sender, instance, *args, **kwargs):
    if instance.passport:
        _delete_file(instance.passport.path)
