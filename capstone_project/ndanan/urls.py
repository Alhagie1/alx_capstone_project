
from django.urls import path
from .views.course_views import CourseDetailView, CourseListView,CourseCreateView
from .views.material_views import MaterialDetailView, MaterialListView,MaterialCreateView
from .views.auth_views import login_view, logout_view,register_view


urlpatterns = [
    path("course_list/", CourseListView.as_view() , name= "Courses"),
    path("course_detail/<int:pk>/", CourseDetailView.as_view(), name="Course details"),
    path("material_list/", MaterialListView.as_view(),name="Materials"),
    path("material_detail/<int:pk>", MaterialDetailView.as_view(), name="Material details"),
    path("login/",login_view, name="Login"),
    path("logout/", logout_view,name="Logout"),
    path("register/", register_view, name="Register"),
    path("course_detail/", CourseCreateView.as_view(), name="create courses" ),
    path("material_detail/", MaterialCreateView.as_view(), name="create material")
]