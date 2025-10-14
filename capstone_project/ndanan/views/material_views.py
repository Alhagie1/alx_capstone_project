
from django.views.generic import ListView, DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from ndanan.models import Material
from django.core.exceptions import PermissionDenied

class TeacherOrAdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user_role = getattr(request.user, 'role', None)
        if user_role not in ["teacher", "admin"]:
            raise PermissionDenied("Only Teachers or Admins can create courses.")
        
        return super().dispatch(request, *args, **kwargs)

#  The material list view class
class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    context_object_name = "material_list"
    template_name = "ndanan/material_list.html"
    paginate_by = 10

# The queryset method that list materials base on the user's role
    def get_queryset(self):
        user = self.request.user
        if user.role == "teacher":
            return Material.objects.filter(teacher = user)
        elif user.role == "student":
            return Material.objects.filter(students = user)
        elif user.role == "admin":
            return Material.objects.all()
        return Material.objects.none()

# The Materila Detail View
class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    context_object_name = "material_detail"
    template_name = "ndanan/material_detail.html"
# The Queryset method that give material details to user based on their roles

    def get_queryset(self):
        user = self.request.user

        if user.role == "teacher":
            return Material.objects.filter(teacher = user)
        elif user.role == "student":
            return Material.objects.filter(students = user)
        elif user.role == "admin":
            return Material.objects.all()
        return Material.objects.none()
# The Material Creation class
class MaterialCreateView(LoginRequiredMixin, TeacherOrAdminRequiredMixin, CreateView):
    model = Material
    context_object_name = "material"
    template_name = "ndanan/material_form.html"
    fields = ["title", "description","course"]

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)
