from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

@login_required(login_url='/login/')

def home(request):

    message = ""
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    
    order = '-created_at'

    if sort == 'old':

        order = 'created_at'

    elif sort == 'name':

        order = 'name'
        
    elif sort == 'new':

        order = '-created_at'    

    if search:

      students = Student.objects.filter(
            user=request.user,
            name__icontains=search
      ).order_by(order)

    else:

      students = Student.objects.filter(
            user=request.user
      ).order_by(order)
      
    total_students = students.count()
    
    paginator = Paginator(students, 2)

    page_number = request.GET.get('page')

    students = paginator.get_page(page_number)

    if request.method == "POST":

        name = request.POST.get('student_name')
        age = request.POST.get('student_age')

        student_image = request.FILES.get('student_image')

        Student.objects.create(

            user=request.user,
            
            name=name,
            age=age,
            image=student_image

        )
        
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
        
        new_image = request.FILES.get('student_image')
        if new_image:

         student.image = new_image

        student.save()

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