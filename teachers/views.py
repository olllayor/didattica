from . import forms, models
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from exams import models as QMODEL
from students import models as SMODEL
from exams import forms as QFORM
from exams import upload_image
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'teachers/teacherclick.html')

def teacher_signup_view(request):
    userForm = forms.TeacherUserForm()
    teacherForm = forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = forms.TeacherUserForm(request.POST)
        teacherForm = forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request, 'teachers/teachersignup.html', context=mydict)

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacher = request.user.teacher   
    dict={
    
    'total_course':QMODEL.Course.objects.filter(creator=teacher).all().count(),
    'teacher_name':teacher.username,
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teachers/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    teacher_courses = QMODEL.Course.objects.filter(creator=request.user.teacher)
    return render(request, 'teachers/teacher_exam.html', {'teacher_courses':teacher_courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method == 'POST':
        courseForm = QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            course = courseForm.save(commit=False)
            course.creator = request.user.teacher
            course.save()
            messages.success(request, 'Course successfully added.')
        else:
            print('error form invalid')

        return HttpResponseRedirect('/teachers/teacher-view-exam')
    return render(request, 'teachers/teacher_add_exam.html', {'courseForm':courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    teacher = request.user.teacher
    courses = QMODEL.Course.objects.filter(creator=teacher)  # Filter courses by the creator
    return render(request, 'teachers/teacher_view_exam.html', {'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course = get_object_or_404(QMODEL.Course, id=pk, creator=request.user.teacher)
    course.delete()
    return JsonResponse({'status': 'success', 'message': 'Course successfully deleted.'})
    # return HttpResponseRedirect('/teachers/teacher-view-exam')

@login_required(login_url='teacherlogin')
def teacher_question_view(request):
    return render(request, 'teachers/teacher_question.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    teacher = request.user.teacher
    # Filter the courses by the logged-in teacher
    teacher_courses = QMODEL.Course.objects.filter(creator=teacher)
    course_exists = teacher_courses.exists()  # This will be False if no courses exist
    questionForm = QFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST, request.FILES)
        if questionForm.is_valid():
            try:                    
                question = questionForm.save(commit=False)
                question.course = questionForm.cleaned_data['courseID']
                image_file = request.FILES.get('picture')
                if image_file:
                    try:
                        image_url = upload_image.upload_image_to_telegraph(image_file)
                        question.picture = image_url
                    except Exception as e:
                        print(e)
                        messages.error(request, 'Failed to upload image. Please try again.')
                        
                question.save()
                return HttpResponseRedirect('/teachers/teacher-view-question')
            except QMODEL.Course.DoesNotExist:
                questionForm.add_error('courseID', 'The selected course does not exist.')
    else:
        questionForm = QFORM.QuestionForm()
        questionForm.fields['courseID'].queryset = teacher_courses  # Set the queryset for courseID field

    return render(request, 'teachers/teacher_add_question.html', {'questionForm':questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    teacher = request.user.teacher
    courses = QMODEL.Course.objects.filter(creator=teacher)
    return render(request, 'teachers/teacher_view_question.html', {'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request, pk):
    
    questions = QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request, 'teachers/see_question.html', {'questions':questions})

from django.http import JsonResponse

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request, pk):
    try:
        question = QMODEL.Question.objects.get(id=pk, course__creator=request.user.teacher)
        question.delete()
        return JsonResponse({'status': 'success', 'message': 'Question successfully deleted.'})
    except QMODEL.Question.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Question not found.'}, status=404)
