from django.db import models
from students.models import Student


# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=80)
    question_number = models.PositiveIntegerField()
    credit = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    creator = models.ForeignKey('teachers.Teacher', related_name='created_courses', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.course_name
    


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    picture = models.ImageField(upload_to='question_pictures', blank=True, null=True)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    option5 = models.CharField(max_length=100, blank=True, null=True)
    answer = models.CharField(max_length=100)
    cat = (('Option1', 'A)'), ('Option2', 'B)'), ('Option3', 'C)'), ('Option4', 'D)'))
    answer = models.CharField(max_length=100, choices=cat)
  

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)