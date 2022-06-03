# Generated by Django 4.0.4 on 2022-05-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_remove_student_others_guardian'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='parent_mobile_number',
            new_name='medical_doctor_number',
        ),
        migrations.RemoveField(
            model_name='student',
            name='medical_doctor',
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_admission',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6),
        ),
    ]
