# Generated by Django 4.0.2 on 2022-04-30 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corecode', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_score', models.IntegerField(default=0)),
                ('exam_score', models.IntegerField(default=0)),
                ('current_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.studentclass')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.academicsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.subject')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.academicterm')),
            ],
            options={
                'ordering': ['subject'],
            },
        ),
    ]
