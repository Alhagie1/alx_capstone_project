from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from ndanan.models import Material, CourseEnrollment
from django.core.exceptions import PermissionDenied

class TeacherOrAdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user_role = getattr(request.user, 'role', None)
        if user_role not in ["teacher", "admin"]:
            raise PermissionDenied("Only Teachers or Admins can create materials.")
        
        return super().dispatch(request, *args, **kwargs)

# The material list view class
class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    context_object_name = "material_list"
    template_name = "ndanan/material_list.html"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        
        if user.role == "admin":
            return Material.objects.all()
        
        elif user.role == "teacher":
            # Materials uploaded by this teacher
            return Material.objects.filter(uploaded_by=user)
        
        elif user.role == "student":
            # Materials from courses the student is enrolled in
            enrolled_courses = CourseEnrollment.objects.filter(
                student=user, 
                is_active=True
            ).values_list('course', flat=True)
            return Material.objects.filter(course__in=enrolled_courses)
        
        return Material.objects.none()

# The Material Detail View
class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    context_object_name = "material_detail"
    template_name = "ndanan/material_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if user.role == "admin":
            return obj
        
        if user.role == "teacher":
            if obj.uploaded_by == user:
                return obj
            else:
                raise PermissionDenied("You are not the uploader of this material.")
        
        if user.role == "student":
            # Check if student is enrolled in the course
            is_enrolled = CourseEnrollment.objects.filter(
                student=user,
                course=obj.course,
                is_active=True
            ).exists()
            
            if is_enrolled:
                return obj
            else:
                raise PermissionDenied("You are not enrolled in this course.")
        
        raise PermissionDenied("You do not have permission to view this material.")

# The Material Creation class
class MaterialCreateView(LoginRequiredMixin, TeacherOrAdminRequiredMixin, CreateView):
    model = Material
    context_object_name = "material"
    template_name = "ndanan/material_form.html"
    fields = ["title", "description", "course", "file"]
    success_url = reverse_lazy("Materials")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)