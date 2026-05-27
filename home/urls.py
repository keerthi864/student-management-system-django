from django.urls import path

from .views import (
    home,
    delete_student,
    update_student,
    student_detail,
    export_students
)

urlpatterns = [
    path('', home),
    path('delete/<int:id>/', delete_student),
    path('update/<int:id>/', update_student),
    path('student/<int:id>/', student_detail),
    path('export/', export_students,
name='export_students'
),
]