
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,CreateView
from ndanan.models import Course, User
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied

class TeacherOrAdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user_role = getattr(request.user, 'role', None)
        if user_role not in ["teacher", "admin"]:
            raise PermissionDenied("Only Teachers or Admins can create courses.")
        
        return super().dispatch(request, *args, **kwargs)


#  The Course List View

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = "course_list"
    template_name = "ndanan/course_list.html"
    paginate_by = 10
# The queryset method that list courses based on the user's role
    def get_queryset(self):
        user = self.request.user

        if user.role == "teacher":
            return Course.objects.filter(teacher = user)
        elif user.role == "student":
            return Course.objects.filter(students = user)
        elif user.role == "admin":
            return Course.objects.all()
        
        return Course.objects.none()


# The Course Detail view class 

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    context_object_name = "course_detail"
    template_name = "ndanan/course_detail.html"
     
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if user.role == "admin":
            return obj 
        
        if user.role == "teacher":
            if obj.teacher == user:
                return obj 
            else:
                raise PermissionDenied("You are not the teacher of this course.")
        
        if user.role == "student":
            if user in obj.students.all(): 
                return obj 
            else:
                raise PermissionDenied("You are not enrolled in this course.")
        
        raise PermissionDenied("You do not have permission to view this course.")


class CourseCreateView(LoginRequiredMixin,TeacherOrAdminRequiredMixin, CreateView):
    model = Course
    template_name = "ndanan/course_form.html" 
    fields = ["name", "description", "course_code"] 
    
    success_url = reverse_lazy("course_detail") 
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)
   