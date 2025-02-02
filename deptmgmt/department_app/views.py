
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from .models import Department, Employee
from .forms import DepartmentForm


# it will check wether the user is admin or not 
def is_admin(user):
    return user.is_authenticated and user.is_staff

# this login view will redirect based on the user or admin 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view:when user will logged out than it will redirect to login page with showing a message that you have been logged out
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')



# Home view: redirects to the proper dashboard based on role
@login_required(login_url='login')
def home(request):
    if request.user.is_staff:
        return redirect('dashboard')
    return redirect('employee_dashboard')

# Admin dashboard: it will allow admin to perforn all the operations 
@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('employee_dashboard')
    departments = Department.objects.filter(status=True)
    search_query = request.GET.get('search', '')
    if search_query:
        departments = departments.filter(dept_name__icontains=search_query)
    return render(request, 'dashboard.html', {'departments': departments})

# Employee dashboard: it will alow user to see the department list only 
@login_required(login_url='login')
def employee_dashboard(request):
    if request.user.is_staff:
        return redirect('dashboard')
    departments = Department.objects.filter(status=True)
    return render(request, 'employee_dashboard.html', {'departments': departments})

# Admin-only : here admin can add the department
@user_passes_test(is_admin, login_url='login')
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully!")
            return redirect('dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'add_department.html', {'form': form})

# Admin-only  : here admin can edit the department
@user_passes_test(is_admin, login_url='login')
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('dashboard')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'edit_department.html', {'form': form})

# Admin-only : here admin can delete the department
@user_passes_test(is_admin, login_url='login')
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    # Check if any employees are assigned to this department
    employees = Employee.objects.filter(department=department)
    if request.method == 'POST':
        if employees.exists():
            messages.error(request, "Cannot delete! There are employees assigned. Reassign them first.")
            return redirect('dashboard')
        department.status = False
        department.save()
        messages.success(request, "Department deleted successfully!")
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'department': department})
