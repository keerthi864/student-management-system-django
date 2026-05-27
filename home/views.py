from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
import openpyxl


@login_required(login_url='/login/')
def home(request):

    message = ""

    search = request.GET.get('search', '')

    sort = request.GET.get('sort', '')

    order = '-created_at'

    # Sorting
    if sort == 'old':

        order = 'created_at'

    elif sort == 'name':

        order = 'name'

    elif sort == 'semester':

        order = 'semester'

    elif sort == 'department':

        order = 'department'

    elif sort == 'age':

        order = 'age'

    elif sort == 'new':

        order = '-created_at'

    # Search students
    if search:

        students = Student.objects.filter(

            Q(name__icontains=search) |

            Q(usn__icontains=search) |

            Q(department__icontains=search) |

            Q(phone__icontains=search),

            user=request.user

        ).order_by(order)

    else:

        students = Student.objects.filter(
            user=request.user
        ).order_by(order)

    # Total student count
    total_students = students.count()

    # Pagination
    paginator = Paginator(students, 2)

    page_number = request.GET.get('page')

    students = paginator.get_page(page_number)

    # Add student
    if request.method == "POST":

        # Get form data
        name = request.POST.get('student_name')

        age = request.POST.get('student_age')

        usn = request.POST.get('student_usn')

        department = request.POST.get('student_department')

        semester = request.POST.get('student_semester')

        phone = request.POST.get('student_phone')

        email = request.POST.get('student_email')

        student_image = request.FILES.get('student_image')

        # Name validation
        if not name:

            messages.error(
                request,
                "Student name is required"
            )

            return redirect('/')

        # Age validation
        if not age:

            messages.error(
                request,
                "Age is required"
            )

            return redirect('/')

        # USN validation
        if not usn:

            messages.error(
                request,
                "USN is required"
            )

            return redirect('/')

        # Department validation
        if not department:

            messages.error(
                request,
                "Department is required"
            )

            return redirect('/')

        # Semester validation
        if not semester:

            messages.error(
                request,
                "Semester is required"
            )

            return redirect('/')

        # Phone validation
        if len(phone) != 10 or not phone.isdigit():

            messages.error(
                request,
                "Phone number must contain exactly 10 digits"
            )

            return redirect('/')

        # Email validation
        if '@' not in email or '.com' not in email:

            messages.error(
                request,
                "Enter valid email address"
            )

            return redirect('/')

        # Image validation
        if not student_image:

            messages.error(
                request,
                "Please upload student image"
            )

            return redirect('/')
        
        if Student.objects.filter(usn=usn).exists():

            messages.error(
                request,
                "USN already exists"
            )

        return redirect('/')


        # Save student
        Student.objects.create(

            user=request.user,

            name=name,

            age=age,

            usn=usn,

            department=department,

            semester=semester,

            phone=phone,

            email=email,

            image=student_image

        )

        # Success message
        messages.success(
            request,
            "Student Added Successfully"
        )

        message = "Student Saved Successfully"

    data = {

        'total_students': total_students,

        'message': message,

        'students': students,

        'sort': sort,

        'search': search

    }

    return render(request, 'home/home.html', data)


def delete_student(request, id):

    student = Student.objects.get(
        id=id,
        user=request.user
    )

    student.delete()

    return redirect('/')


def update_student(request, id):

    student = Student.objects.get(
        id=id,
        user=request.user
    )

    if request.method == "POST":

        student.name = request.POST.get('student_name')

        student.age = request.POST.get('student_age')

        student.usn = request.POST.get('student_usn')

        student.department = request.POST.get('student_department')

        student.semester = request.POST.get('student_semester')

        student.phone = request.POST.get('student_phone')

        student.email = request.POST.get('student_email')

        # Update image
        new_image = request.FILES.get('student_image')

        if new_image:

            student.image = new_image

        student.save()

        messages.success(
            request,
            "Student Updated Successfully"
        )

        return redirect('/')

    data = {
        'student': student
    }

    return render(request, 'home/update.html', data)


@login_required(login_url='/login/')
def student_detail(request, id):

    student = Student.objects.get(id=id)

    data = {
        'student': student
    }

    return render(
        request,
        'home/detail.html',
        data
    )


def register(request):

    if request.method == "POST":

        username = request.POST['username']

        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'accounts/register.html')

def export_students(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Students"

    # Headers
    headers = [
        "Name",
        "Age",
        "USN",
        "Department",
        "Semester",
        "Phone",
        "Email"
    ]

    sheet.append(headers)

    students = Student.objects.filter(user=request.user)

    for student in students:

        sheet.append([

            student.name,
            student.age,
            student.usn,
            student.department,
            student.semester,
            student.phone,
            student.email

        ])

    response = HttpResponse(
        content_type='application/ms-excel'
    )

    response['Content-Disposition'] = (
        'attachment; filename="students.xlsx"'
    )

    workbook.save(response)

    return response