#coding: utf-8

from django import forms
from courses.models import DefaultTeacher
import os

class PdfForm(forms.Form):
    pdf = forms.FileField(required=False)
    def __init__(self, *args, **kwargs):
        self.extensions = kwargs.pop('extensions', None)
        super(PdfForm, self).__init__(*args, **kwargs)
    def clean_pdf(self):
        file = self.cleaned_data.get('pdf')
        if file:
            name, extension = os.path.splitext(file.name)
            if extension not in self.extensions:
                raise forms.ValidationError(u'Файл должен иметь одно из расширений: ' + ",".join(self.extensions))


class QueueForm(forms.Form):
    rework = forms.BooleanField(initial=False, label='На доработке', required=False)
    verefication = forms.BooleanField(initial=True, label='На проверке', required=False)
    need_info = forms.BooleanField(initial=False, label='Требуется информация', required=False)
    mine = forms.BooleanField(initial=True, label='Мои задачи', required=False)
    following = forms.BooleanField(initial=True, label='Наблюдаемые мной', required=False)
    not_mine = forms.BooleanField(initial=True, label='Не мои', required=False)
    not_owned = forms.BooleanField(initial=True, label='Ничьи', required=False)
    overdue = forms.IntegerField(initial=0, label='Ждут проверки несколько дней')

def get_teacher_choises(course):
    teachers = [(0, "(None)")]
    for teacher in course.get_teachers():
        teachers.append((teacher.id, teacher.get_full_name()))
    return teachers

class DefaultTeacherForm(forms.Form):
    def __init__(self, course, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)

        self.groups = {}
        self.teachers = get_teacher_choises(course)
        groups_teacher = {}
        for default_teacher in DefaultTeacher.objects.filter(group__in=course.groups.all()):
            groups_teacher[default_teacher.group.id] = default_teacher.teacher.id

        for group in course.groups.all():
            group_key = "group_{0}".format(group.id)
            self.groups[group_key] = group
            self.fields[group_key] = forms.ChoiceField(initial=groups_teacher.get(group.id, 0), choices=self.teachers, label=group.name)

def default_teacher_forms_factory(course, group, teacher=None, post_data=None):
    teacher_id = 0
    if teacher:
        teacher_id = teacher.id

    class DefaultTeacherForm(forms.Form):
        course_id = forms.IntegerField(initial=course.id, widget=forms.HiddenInput)
        groups_id = forms.IntegerField(initial=group.id, widget=forms.HiddenInput)
        teacher = forms.ChoiceField(initial=teacher_id, choices=get_teacher_choises(course), label="")
    return DefaultTeacherForm()
