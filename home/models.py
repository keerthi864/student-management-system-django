from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Student(models.Model):
    
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    age = models.IntegerField()
    
    image = models.ImageField(upload_to='students/')
    
    created_at = models.DateTimeField(default=now)