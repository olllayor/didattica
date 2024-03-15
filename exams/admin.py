from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ['course_name', 'creator', 'is_available', 'available_from', 'available_until']
#     list_filter = ['is_available']
#     search_fields = ['course_name', 'creator__user__username']
