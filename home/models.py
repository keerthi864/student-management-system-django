from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Student(models.Model):
    
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
    )
    
    email = models.EmailField()

    name = models.CharField(max_length=100)

    age = models.IntegerField()
    
    image = models.ImageField(upload_to='students/')
    
    usn = models.CharField(max_length=20)

    department = models.CharField(max_length=100)

    semester = models.IntegerField()

    phone = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(default=now)