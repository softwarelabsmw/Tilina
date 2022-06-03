from django.forms import inlineformset_factory, modelformset_factory

from .models import Student, Guardian

StudentGuardianFormset = inlineformset_factory(
    Student, Guardian,
    fields=["full_name", "gender", "relation", "occupation", "mobile_number", "email"],
    extra=1,
    max_num=2,
    absolute_max=2,
    can_delete=True
)

Students = modelformset_factory(Student, exclude=(), extra=4)

