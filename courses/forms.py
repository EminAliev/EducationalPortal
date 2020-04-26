from django.forms.models import inlineformset_factory

from courses.models import Course, Module

CourseModuleFormSet = inlineformset_factory(Course, Module, fields=['name', 'definition'], extra=2, can_delete=True)
