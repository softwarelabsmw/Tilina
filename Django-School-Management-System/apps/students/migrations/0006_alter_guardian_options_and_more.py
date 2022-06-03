# Generated by Django 4.0.4 on 2022-05-09 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_alter_guardian_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guardian',
            options={},
        ),
        migrations.RenameField(
            model_name='guardian',
            old_name='parent_mobile_number',
            new_name='mobile_number',
        ),
        migrations.AlterField(
            model_name='guardian',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Residential Address'),
        ),
        migrations.AlterField(
            model_name='guardian',
            name='relation',
            field=models.CharField(choices=[('mother', 'Mother'), ('father', 'Father')], default='father', max_length=10),
        ),
        migrations.AlterField(
            model_name='guardian',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='students.student'),
            preserve_default=False,
        ),
    ]