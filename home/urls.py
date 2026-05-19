from django.urls import path
from .views import (
    home,
    delete_student,
    update_student,
    student_detail
)

urlpatterns = [
    path('', home),
    path('delete/<int:id>/', delete_student),
    path('update/<int:id>/', update_student),
    path('student/<int:id>/', student_detail),
]