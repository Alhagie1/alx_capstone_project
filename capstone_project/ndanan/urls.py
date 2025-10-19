
from django.urls import path
from .views.course_views import CourseDetailView, CourseListView,CourseCreateView
from .views.material_views import MaterialDetailView, MaterialListView,MaterialCreateView
from .views.auth_views import login_view, logout_view,register_view, home_view

urlpatterns = [
    path("", home_view, name="home"),  
    path("course_list/", CourseListView.as_view() , name= "course_list"),
    path("course_detail/<int:pk>/", CourseDetailView.as_view(), name="course_details"),
    path("material_list/", MaterialListView.as_view(),name="material_list"),
    path("material_detail/<int:pk>", MaterialDetailView.as_view(), name="material_details"),
    path("login/",login_view, name="Login"),
    path("logout/", logout_view,name="Logout"),
    path("register/", register_view, name="Register"),
    path("course_create/", CourseCreateView.as_view(), name="course_create" ),
    path("material_create/", MaterialCreateView.as_view(), name="material_create"),
    
]