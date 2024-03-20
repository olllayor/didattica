from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/Students', null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False, unique=True)
    @property
    def get_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    @property
    def get_institute(self):
        return self
    @property
    def username(self):
        return self.user.username
    @property
    def get_mobile(self):
        return self.mobile
    
    def __str__(self):
        return self.user.first_name
    
