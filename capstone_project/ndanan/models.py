from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=64, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='ndanan_user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='ndanan_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email


class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses')

    def __str__(self):
        return self.course_code


class Material(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="uploaded_materials")
    
    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    max_score = models.FloatField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="assignments")

    def __str__(self):
        return f"title:{self.title}, course:{self.course} and description:{self.description}"



class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_courses')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.course


class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('pending', 'Pending'),
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='pending')
    submission_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    score = models.FloatField()
    feedback = models.TextField(blank=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    graded_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name="grades")

    def __str__(self):
        return self.score