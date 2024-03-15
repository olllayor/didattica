from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))

class TeacherSalaryForm(forms.Form):
    salary = forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['course_name', 'question_number','total_marks', 'credit']

class QuestionForm(forms.ModelForm):
    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(), empty_label="Select Course", to_field_name="id")
    image_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Question
        fields = ['courseID', 'marks', 'question', 'picture', 'option1', 'option2', 'option3', 'option4','option5', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            # Add other widgets here as needed
        }


class AIQuestionForm(forms.Form):
    user_input = forms.CharField(widget=forms.HiddenInput())
