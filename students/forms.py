from django import forms
from django.contrib.auth.models import User
from . import models
class StudentUserForm(forms.ModelForm):
    student_id = forms.CharField(max_length=10) 
    class Meta:
        model=User
        fields = ['first_name', 'last_name','username', 'password', 'student_id']
        widgets = {
            'password': forms.PasswordInput()
        }

    




class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = ['profile_pic', 'mobile','student_id']

