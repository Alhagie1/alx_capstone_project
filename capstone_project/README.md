# Ndanan - School Learning Platform

A comprehensive Django-based learning management system designed for educational institutions to manage courses, assignments, materials, and student-teacher interactions.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [User Roles](#-user-roles)
- [API Documentation](#-api-documentation)
- [Database Models](#-database-models)
- [Security Features](#-security-features)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## ✨ Features

### For Teachers
- **Course Management**: Create, update, and manage multiple courses
- **Material Distribution**: Upload and share course materials (PDFs, documents, presentations) with students
- **Assignment Creation**: Create assignments with configurable due dates and scoring systems
- **Grade Management**: Review student submissions and provide detailed grades with feedback
- **Student Oversight**: View and manage enrolled students across all courses

### For Students
- **Course Enrollment**: Browse and enroll in available courses
- **Resource Access**: Download and view course materials anytime
- **Assignment Submission**: Submit assignments before due dates with automatic late detection
- **Grade Tracking**: View grades and instructor feedback in real-time
- **Personalized Dashboard**: Access all enrolled courses from a centralized interface

### For Administrators
- **System Administration**: Full access to all courses, users, and platform content
- **User Management**: Create and manage teacher and student accounts with role assignments
- **Platform Oversight**: Monitor all activities and maintain system integrity

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | Django 5.2.5 |
| **API Layer** | Django Rest Framework (DRF) |
| **Database** | MySQL (development/production) |
| **Frontend** | HTML, CSS (Tailwind CSS), JavaScript |
| **Authentication** | Django Authentication System |
| **Python Version** | 3.13.3 |

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (recommended)
- Git

### Step-by-Step Setup

**1. Clone the Repository**
```bash
git clone https://github.com/yourusername/ndanan.git
cd ndanan
```

**2. Create and Activate Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL Database Configuration
DB_NAME=ndanan_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

**5. Initialize Database**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create Admin Account**
```bash
python manage.py createsuperuser
```

**7. Start Development Server**
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser to access the platform.

---

## ⚙️ Configuration

### Key Settings

Located in `capstone_project/settings.py`:

- **MEDIA_ROOT**: Directory for user-uploaded files (profiles, materials, submissions)
- **STATIC_ROOT**: Directory for static assets (CSS, JavaScript, images)
- **AUTH_USER_MODEL**: Custom user model (`ndanan.User`)

### Custom User Model

Role-based access control with three user types:

```python
ROLE_CHOICES = [
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('admin', 'Admin'),
]
```

---

## 🚀 Usage

### Creating a Course (Teacher/Admin)

1. Log in as a teacher or administrator
2. Navigate to the "Courses" page
3. Click "Create Course" button
4. Fill in the required details:
   - Course Name
   - Course Code (must be unique)
   - Description
5. Submit to create the course

### Uploading Materials (Teacher)

1. Navigate to your course page
2. Click "Add Material"
3. Select a file and provide:
   - Title
   - Description (optional)
4. Submit to make it instantly available to enrolled students

### Enrolling in Courses (Student)

1. Browse available courses from the dashboard
2. Click "Enroll" on desired courses
3. Access materials and assignments immediately after enrollment

---

## 📁 Project Structure

```
ndanan/
├── capstone_project/          # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py               # Root URL routing
│   └── wsgi.py               # WSGI application
│
├── ndanan/                    # Main application
│   ├── models.py             # Database models
│   ├── serializers.py        # DRF serializers for API
│   ├── forms.py              # Django forms
│   ├── urls.py               # Application URL routing
│   ├── views/
│   │   ├── auth_views.py     # Authentication views
│   │   ├── course_views.py   # Course management
│   │   └── material_views.py # Material management
│   └── templates/
│       └── ndanan/           # HTML templates
│
├── media/                     # User-uploaded files
│   ├── profiles/             # Profile pictures
│   ├── materials/            # Course materials
│   └── submissions/          # Assignment submissions
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 👥 User Roles

### Administrator
- Full system access and control
- Manage all users, courses, and content
- System-wide monitoring and oversight
- Access to Django admin panel

### Teacher
- Create and manage personal courses
- Upload materials and create assignments
- Grade student submissions with feedback
- View enrolled students and their progress

### Student
- Enroll in available courses
- Access and download course materials
- Submit assignments before deadlines
- View grades and instructor feedback

---

## 🔗 API Documentation

The platform provides a RESTful API built with Django Rest Framework for headless operations and frontend integration.

> **Implementation Status**: ✅ = Fully Implemented | 🔄 = Planned (Serializers Ready)

---

### ✅ Authentication Endpoints (Implemented)

**POST** `/api/auth/login/`  
Authenticate user and obtain token  
**Serializer**: `LoginSerializer`

**POST** `/api/auth/register/`  
Register new user account  
**Serializer**: `UserRegistrationSerializer`

**GET** `/api/auth/profile/`  
View and update user profile  
**Serializer**: `UserProfileSerializer`

---

### ✅ Course Endpoints (Implemented)

**GET** `/api/courses/`  
List all available courses  
**Serializer**: `CourseListSerializer`

**GET** `/api/courses/<id>/`  
Retrieve detailed information about a specific course  
**Serializer**: `CourseDetailSerializer`

**POST** `/api/courses/create/`  
Create a new course (Teacher/Admin only)  
**Serializer**: `CourseCreateSerializer`

---

### ✅ Material Endpoints (Implemented)

**GET** `/api/materials/`  
List all course materials  
**Serializer**: `MaterialSerializer`

**POST** `/api/materials/create/`  
Upload new course material  
**Serializer**: `MaterialSerializer`

**GET** `/api/materials/<id>/`  
Retrieve specific material details  
**Serializer**: `MaterialSerializer`

---

### 🔄 Assignment Endpoints (Planned - Serializers Ready)

**GET** `/api/assignments/`  
List all assignments  
**Serializer**: `AssignmentListSerializer` ✓

**POST** `/api/assignments/create/`  
Create new assignment (Teacher only)  
**Serializer**: `AssignmentCreateSerializer` ✓

**GET** `/api/assignments/<id>/`  
Get assignment details with submissions  
**Serializer**: `AssignmentDetailSerializer` ✓

---

### 🔄 Submission Endpoints (Planned - Serializers Ready)

**POST** `/api/submissions/`  
Submit an assignment (Student only)  
**Serializer**: `SubmissionSerializer` ✓

**GET** `/api/submissions/assignment/<id>/`  
List all submissions for an assignment (Teacher only)  
**Serializer**: `SubmissionListSerializer` ✓

---

### 🔄 Grade Endpoints (Planned - Serializers Ready)

**POST** `/api/grades/`  
Create or update a grade (Teacher only)  
**Serializer**: `GradeSerializer` ✓

**GET** `/api/grades/<id>/`  
Retrieve grade details  
**Serializer**: `GradeSerializer` ✓

---

## 💻 DRF Serializers Overview

### User Serializers

| Serializer | Purpose | Key Features |
|------------|---------|--------------|
| `UserSerializer` | Basic user information display | Includes calculated `full_name` field |
| `UserRegistrationSerializer` | New user registration | Password validation, requires matching passwords |
| `UserProfileSerializer` | Profile updates | Read-only email, role, and join date |
| `LoginSerializer` | Authentication | Email/password validation |

### Course Serializers

| Serializer | Purpose | Key Features |
|------------|---------|--------------|
| `CourseListSerializer` | Course list view | Includes `teacher_name` and `student_count` |
| `CourseDetailSerializer` | Single course details | Nested teacher info, material/assignment counts |
| `CourseCreateSerializer` | Course creation | Auto-assigns logged-in user as teacher |

### Material Serializers

| Serializer | Purpose | Key Features |
|------------|---------|--------------|
| `MaterialSerializer` | Material management | Includes `course_name` and `uploaded_by_name` |

### Assignment Serializers

| Serializer | Purpose | Key Features |
|------------|---------|--------------|
| `AssignmentListSerializer` | Assignment list view | Calculates `submission_count` and `is_overdue` |
| `AssignmentDetailSerializer` | Assignment details | Nested course/user info, grading statistics |
| `AssignmentCreateSerializer` | Assignment creation | Validates max_score and due_date |

### Submission & Grade Serializers

| Serializer | Purpose | Key Features |
|------------|---------|--------------|
| `SubmissionSerializer` | Assignment submission | 5MB file limit, automatic late detection |
| `SubmissionListSerializer` | Submission tracking | Includes `has_grade` boolean |
| `GradeSerializer` | Grade management | Validates score against max_score |
| `GradeCreateSerializer` | Grade creation | Simple score and feedback input |

---

## 📝 Database Models

### Core Models

- **User**: Custom user model with email authentication and role-based access
- **Course**: Academic courses with teacher assignments and enrollment tracking
- **Material**: Course materials uploaded by teachers
- **Assignment**: Assignments with due dates and scoring systems
- **CourseEnrollment**: Student enrollment records
- **Submission**: Student assignment submissions with file storage
- **Grade**: Grades and feedback for submissions

---

## 🔒 Security Features

- CSRF protection enabled on all forms
- Password hashing using Django's built-in authentication
- Role-based access control (RBAC)
- Permission checks on all sensitive views
- Secure file upload handling with size limits (5MB)
- Password validation during registration
- SQL injection protection via Django ORM

---

## 🐛 Troubleshooting

### Common Issues

**NoReverseMatch Error**
- **Cause**: URL name mismatch in templates or views
- **Solution**: Verify URL names in `urls.py` match template references

**Course Creation Fails**
- **Cause**: Insufficient permissions
- **Solution**: Ensure user has 'teacher' or 'admin' role

**File Upload Fails**
- **Cause**: Permission or size issues
- **Solution**: Check `MEDIA_ROOT` directory permissions and ensure files are under 5MB

**Migration Errors**
- **Cause**: Database inconsistencies
- **Solution**: Delete migration files (except `__init__.py`) and `db.sqlite3`, then re-run migrations

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. **Open** a Pull Request

### Coding Standards

- Follow **PEP 8** style guidelines
- Write **descriptive commit messages**
- Add **comments** for complex logic
- **Update documentation** when adding features
- Write **tests** for new functionality

---

## 📧 Contact

**Developer**: Alhagie Nyang  
**Email**: alhagienyang13@gmail.com  
**Project Repository**: [https://github.com/Alhagie1/ndanan](https://github.com/Alhagie1/ndanan)

---

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- All contributors and testers

---

## 📄 License

This project is built for educational purposes as a capstone project. For production deployment, additional security measures and optimizations are recommended.

---

**Note**: This is an educational capstone project. Before deploying to production, implement additional security hardening, performance optimization, and comprehensive testing.