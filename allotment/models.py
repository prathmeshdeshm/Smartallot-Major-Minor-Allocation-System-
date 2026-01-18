from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """
    Student model for storing student information.
    """
    DEPARTMENTS = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=10, choices=DEPARTMENTS)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    class Meta:
        ordering = ['-percentage']
