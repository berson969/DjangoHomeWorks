from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    objects_list = Student.objects.all().prefetch_related('teachers')
    # teachers_list = students_list.teachers.all()
    context = {
        'object_list': objects_list,
        # 'teachers_list': teachers_list

    }

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'

    return render(request, template, context)
