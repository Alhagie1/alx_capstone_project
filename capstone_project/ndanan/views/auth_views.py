from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ndanan.forms import RegistrationForm
from ndanan.models import User


def generate_email(user):
    """
    Generating email from user's data
    """
    first = user.first_name.replace(" ", "").lower()
    last = user.last_name.replace(" ", "").lower()

    if user.role == "teacher":
        domain = "staff.school.com"
    else:  
        domain = "school.edu"
    
    email = f"{first}{last}{user.id}@{domain}"
    return email


def login_view(request):
    if request.user.is_authenticated:
        return redirect("user:profile")
    
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        
        if not email or not password:
            messages.error(request, "Email and password are required")
            return redirect("login")
        
        # Use 'username' parameter even though USERNAME_FIELD is 'email'
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully!")
            next_url = request.GET.get('next', 'user:profile')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")
        
    return render(request, "login.html")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("login")
    return render(request, "logout.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("user:profile")
    
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()  
            
            # Generate and set email
            user.email = generate_email(user)
            user.save(update_fields=['email'])
            
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}! Registration successful.")

            if user.role == "teacher":
                return redirect("teacher-dashboard")
            else:
                return redirect("student-dashboard")
        else:
            return redirect(request, "register.html", {"form":form})
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})