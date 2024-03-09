from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate
from . import forms, models
from exams import models as QMODEL
from students import models as SMODEL
from exams import forms as QFORM
# Create your views here.

def studentclick_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'students/studentclick.html')

def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userFrom':userForm, 'studentForm': studentForm}

    if request.method=="POST":
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(userForm.cleaned_data['password'])
            user.save()

            student = studentForm.save(commit=False)
            student.user = user
            student.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return  HttpResponseRedirect('studentlogin')
    return render(request, 'students/studentsignup.html', context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict = {
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
    }
    return render(request, 'students/student_dashboard.html', context=dict)
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_pro_view(request):
    # student = models.Student.objects.get(user_id=request.user.id)
    return render(request, 'students/student_pro.html')


# In views.py within the student_exam_view

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.select_related('creator').all()
    return render(request, 'students/student_exam.html', {'courses': courses})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course = QMODEL.Course.objects.select_related("creator").get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = sum(q.marks for q in questions)
    teacher_name = course.creator.get_name
    return render(
        request,
        'students/take_exam.html',
        {'course':course, 'total_questions':total_questions, 'total_marks':total_marks, 'teacher_name': teacher_name}
        )

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    course = get_object_or_404(QMODEL.Course, id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'students/start_exam.html', {'course':course, 'questions':questions})
    response.set_cookie('course_id', course.id)
    return response

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)
        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        
        for i in range(len(questions)):
            selected_ans = request.COOKIES.get(str(i+1))
            actual_ans = questions[i].answer
            if selected_ans == actual_ans:
                total_marks += questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        result.save()

        return HttpResponseRedirect('view-result')
    
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    
    return render(request, 'students/view_result.html', {'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course = QMODEL.Course.objects.select_related("creator").get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    teacher_name = course.creator.get_name
    return render(request, 'students/check_marks.html', {'results':results, 'teacher_name':teacher_name})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.select_related('creator').all()
    return render(request, 'students/student_marks.html', {'courses':courses})
