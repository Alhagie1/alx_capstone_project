from django.contrib import admin
from .models import User, Course, Submission, Grade,Assignment,Material,CourseEnrollment

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Material)
admin.site.register(CourseEnrollment)
admin.site.register(Assignment)
admin.site.register(Submission)
