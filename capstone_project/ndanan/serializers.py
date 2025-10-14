from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Course, Assignment, Material, CourseEnrollment, Submission, Grade
from django.utils import timezone

#  USER SERIALIZERS 

class UserSerializer(serializers.ModelSerializer):
    """Basic user info - safe for general display"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "full_name", "role", "profile_picture"]
        read_only_fields = ["id"]
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class UserRegistrationSerializer(serializers.ModelSerializer):
    """For user registration - includes password handling"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ["email", "password", "password2", "first_name", "last_name", "role"]
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Password do not match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """For viewing/updating own profile"""
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "profile_picture", 'date_joined']
        read_only_fields = ["id", "email", "role", "date_joined"]


# COURSE SERIALIZERS

class CourseListSerializer(serializers.ModelSerializer):
    """For listing courses - includes teacher name and student count"""
    teacher_name = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ["id", "name", "course_code", "description", "teacher", "teacher_name", 
                  "student_count", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
    
    def get_teacher_name(self, obj):
        return f"{obj.teacher.first_name} {obj.teacher.last_name}"
    
    def get_student_count(self, obj):
        return obj.enrollments.filter(is_active=True).count()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Detailed course view with enrolled students"""
    teacher = UserSerializer(read_only=True)
    enrolled_students = serializers.SerializerMethodField()
    material_count = serializers.SerializerMethodField()
    assignment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ["id", "name", "course_code", "description", "teacher", 
                  "enrolled_students", "material_count", "assignment_count",
                  "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "teacher", "created_at", "updated_at"]
    
    def get_enrolled_students(self, obj):
        enrollments = obj.enrollments.filter(is_active=True)
        return UserSerializer([e.student for e in enrollments], many=True).data
    
    def get_material_count(self, obj):
        return obj.materials.count()
    
    def get_assignment_count(self, obj):
        return obj.assignments.count()


class CourseCreateSerializer(serializers.ModelSerializer):
    """For creating courses - teacher auto-assigned from request"""
    class Meta:
        model = Course
        fields = ['name', 'course_code', 'description', 'is_active']
    
    def create(self, validated_data):
        # Teacher is automatically set from the request user
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)


# MATERIAL SERIALIZERS 

class MaterialSerializer(serializers.ModelSerializer):
    """For material uploads and viewing"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Material
        fields = ["id", "course", "course_name", "title", "description", "file", 
                  "uploaded_by", "uploaded_by_name", "created_at", "updated_at"]
        read_only_fields = ["id", "uploaded_by", "created_at", "updated_at"]
    
    def get_uploaded_by_name(self, obj):
        return f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}"
    
    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        return super().create(validated_data)


# ASSIGNMENT SERIALIZERS

class AssignmentListSerializer(serializers.ModelSerializer):
    """For listing assignments"""
    course_name = serializers.CharField(source="course.name", read_only=True)
    submission_count = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = ["id", "course", "course_name", "title", "description", "due_date", 
                  "max_score", "submission_count", "is_overdue", "created_at", "created_by"]
        read_only_fields = ["id", "created_at", "created_by"]
    
    def get_submission_count(self, obj):
        return obj.submissions.count()
    
    def get_is_overdue(self, obj):
        if obj.due_date:
            return timezone.now() > obj.due_date
        return False
    


class AssignmentDetailSerializer(serializers.ModelSerializer):
    """Detailed assignment view"""
    course = CourseListSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    submission_count = serializers.SerializerMethodField()
    graded_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = ["id", "course", "title", "description", "due_date", "max_score", 
                  "created_by", "submission_count", "graded_count", "created_at", "updated_at"]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
    
    def get_submission_count(self, obj):
        return obj.submissions.count()
    
    def get_graded_count(self, obj):
        return obj.submissions.filter(status="graded").count()


class AssignmentCreateSerializer(serializers.ModelSerializer):
    """For creating assignments"""
    class Meta:
        model = Assignment
        fields = ["course", "title", "description", "due_date", "max_score"]
    
    def validate_max_score(self, value):
        if value <= 0:
            raise serializers.ValidationError("Max score must be greater than 0")
        return value
    
    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
    
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


# ENROLLMENT SERIALIZERS

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """For managing course enrollments"""
    student = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = CourseEnrollment
        fields = ["id", "course", "student", "enrolled_at", "is_active"]
        read_only_fields = ["id", "enrolled_at"]


class EnrollStudentSerializer(serializers.Serializer):
    """For enrolling a student in a course"""
    student_id = serializers.IntegerField()
    
    def validate_student_id(self, value):
        try:
            user = User.objects.get(id=value)
            if user.role != "student":
                raise serializers.ValidationError("User must be a student")
        except User.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        return value


# SUBMISSION SERIALIZERS

class SubmissionSerializer(serializers.ModelSerializer):
    """For student submissions"""
    assignment_title = serializers.CharField(source="assignment.title", read_only=True)
    student_name = serializers.SerializerMethodField()
    is_late = serializers.SerializerMethodField()
    grade_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ["id", "assignment", "assignment_title", "student", "student_name", 
                  "submission_file", "submitted_at", "status", "is_late", "grade_info"]
        read_only_fields = ["id", "student", "submitted_at", "status"]
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    
    def get_is_late(self, obj):
        if obj.assignment.due_date:
            return obj.submitted_at > obj.assignment.due_date
        return False
    
    def get_grade_info(self, obj):
        try:
            grade = obj.grade
            return {
                "score": grade.score,
                "feedback": grade.feedback,
                "graded_at": grade.graded_at
            }
        except Grade.DoesNotExist:
            return None
    
    def validate_submission_file(self, value):
        # Limiting the file size to 5MB for submissions
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Submission file cannot exceed 5MB")
        return value
    
    def create(self, validated_data):
        from django.utils import timezone
        validated_data["student"] = self.context["request"].user
        validated_data["submitted_at"] = timezone.now()
        
        # Check if late
        assignment = validated_data["assignment"]
        if assignment.due_date and validated_data["submitted_at"] > assignment.due_date:
            validated_data["status"] = "submitted"  
        else:
            validated_data["status"] = "submitted"
        
        return super().create(validated_data)


class SubmissionListSerializer(serializers.ModelSerializer):
    """Simplified submission list for teachers"""
    student = UserSerializer(read_only=True)
    assignment_title = serializers.CharField(source="assignment.title", read_only=True)
    has_grade = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ["id", "assignment", "assignment_title", "student", "submitted_at", "status", "has_grade"]
        read_only_fields = ["id"]
    
    def get_has_grade(self, obj):
        return hasattr(obj, "grade")


# GRADE SERIALIZERS

class GradeSerializer(serializers.ModelSerializer):
    """For viewing grades with submission details"""
    student_name = serializers.SerializerMethodField()
    assignment_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Grade
        fields = ["id", "submission","student_name", "assignment_title",
                  "score", "feedback", "graded_at", "updated_at"]
        read_only_fields = ["id", "graded_at", "updated_at"]
    
    def get_student_name(self, obj):
        return f"{obj.submission.student.first_name} {obj.submission.student.last_name}"
    
    def get_assignment_title(self, obj):
        return obj.submission.assignment.title
    
    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score cannot be negative")
        return value
    
    def validate(self, data):
        # Get the submission to check max_score
        submission = data.get("submission") or self.instance.submission
        score = data.get("score")
        max_score = submission.assignment.max_score
        
        if score > max_score:
            raise serializers.ValidationError({
                "score": f"Score cannot be greater than the max score of {max_score}"
            })
        
        return data
    
    def create(self, validated_data):
        # Update submission status to graded
        submission = validated_data["submission"]
        submission.status = "graded"
        submission.save()
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Keep submission as graded
        instance.submission.status = "graded"
        instance.submission.save()
        
        return super().update(instance, validated_data)


class GradeCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating/updating grades"""
    class Meta:
        model = Grade
        fields = ["score", "feedback"]
    
    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score cannot be negative")
        return value
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)