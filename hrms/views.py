from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserForm, LeaveRequestForm, EmployeeProfileForm, AttendanceForm, LeaveForm, EmployeeForm, PerformanceReviewForm, NoticeForm
from .models import User, Payslip, Salary, Employee, Attendance, Leave, PerformanceReview, Notice, Department

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = EmployeeProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = EmployeeProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def dashboard(request):
    if request.user.is_admin:
        total_employees = Employee.objects.count()
        departments = Department.objects.all()
        today = timezone.now().date()
        present_employees = Attendance.objects.filter(date=today, time_out__isnull=True).count()
        return render(request, 'admin_dashboard.html', {
            'total_employees': total_employees,
            'departments': departments,
            'present_employees': present_employees,
        })
    else:
        return render(request, 'employee_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_admin)
def manage_employees(request):
    employees = Employee.objects.all()
    return render(request, 'manage_employees.html', {'employees': employees})

@login_required
def add_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.is_employee = True
            user.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('manage_employees')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()

    return render(request, 'add_employee.html', {
        'user_form': user_form,
        'employee_form': employee_form
    })

def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('manage_employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})

def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.delete()
        return redirect('manage_employees')
    return render(request, 'delete_employee.html', {'employee': employee})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.employee = request.user.employee
            attendance.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'mark_attendance.html', {'form': form})

@login_required
def attendance_list(request):
    if request.user.is_admin:
        attendances = Attendance.objects.all()
    else:
        attendances = Attendance.objects.filter(employee=request.user.employee)
    return render(request, 'attendance_list.html', {'attendances': attendances})

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the attendance list page or another appropriate view
            return redirect('attendance_list')  # Assuming 'attendance_list' is your list view
    else:
        form = AttendanceForm()

    return render(request, 'add_attendance.html', {'form': form})

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST, request.FILES)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user.employee
            leave.status = 'PENDING'
            leave.save()
            return redirect('leave_list')
    else:
        form = LeaveForm()
    return render(request, 'apply_leave.html', {'form': form})

@login_required
def leave_list(request):
    if request.user.is_admin:
        leaves = Leave.objects.all()
    else:
        leaves = Leave.objects.filter(employee=request.user.employee)
    return render(request, 'leave_list.html', {'leaves': leaves})

@login_required
@user_passes_test(lambda u: u.is_admin)
def manage_leaves(request):
    leaves = Leave.objects.all()
    return render(request, 'manage_leaves.html', {'leaves': leaves})

@login_required
def submit_performance_review(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.employee = employee
            review.save()
            return redirect('employee_details', employee_id=employee.id)
    else:
        form = PerformanceReviewForm()
    return render(request, 'submit_performance_review.html', {'form': form, 'employee': employee})

@login_required
def view_notices(request):
    notices = Notice.objects.all().order_by('-date_posted')
    return render(request, 'view_notices.html', {'notices': notices})

@login_required
@user_passes_test(lambda u: u.is_admin)
def post_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_notices')
    else:
        form = NoticeForm()
    return render(request, 'post_notice.html', {'form': form})

def recruitment_management(request):
    # Add your logic here
    # For example, fetching data from models or performing operations
    context = {
        'page_title': 'Recruitment Management',  # Example context data
        # Add more context data as needed
    }
    return render(request, 'recruitment_management.html', context)

def training_management(request):
    # Your view logic here
    return render(request, 'training_management.html', {})

def awards_management(request):
    # View logic goes here
    return render(request, 'awards_management.html')

def settings_view(request):
    # Add your logic here to render the settings page
    return render(request, 'settings.html', {})

@login_required
def performance_management(request):
    # Retrieve all employees and their performance reviews
    employees = Employee.objects.all()
    performance_reviews = PerformanceReview.objects.all()

    context = {
        'employees': employees,
        'performance_reviews': performance_reviews,
    }

    return render(request, 'performance_management.html', context)

def payroll_management(request):
    # Your logic here
    return render(request, 'payroll_management.html')

def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')

def documents(request):
    # your view logic
    return render(request, 'documents.html')

def time_sheet(request):
    return render(request, 'time_sheet.html')

def leave_requests(request):
    # Your view logic here
    return render(request, 'leave_requests.html')

@login_required
def employee_dashboard(request):
    employee = request.user.employee
    context = {
        'employee': employee,
    }
    return render(request, 'employee/dashboard.html', context)

@login_required
def employee_profile(request):
    employee = request.user.employee
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
    else:
        form = EmployeeProfileForm(instance=employee)

    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, 'profile.html', context)

@login_required
def employee_attendance(request):
    employee = request.user.employee
    today = timezone.now().date()
    attendance = Attendance.objects.filter(employee=employee, date=today).first()

    if request.method == 'POST':
        if not attendance:
            attendance = Attendance.objects.create(employee=employee, date=today)
        else:
            attendance.time_out = timezone.now().time()
            attendance.save()

    context = {
        'attendance': attendance,
    }
    return render(request, 'attendance.html', context)

def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'edit_attendance.html', {'form': form})

@login_required
def check_in_out(request):
    employee = request.user.employee
    today = timezone.now().date()
    current_time = timezone.now().time()
    location = request.POST.get('location', '')

    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today,
        defaults={'time_in': current_time, 'location_in': location}
    )

    if not created:
        attendance.time_out = current_time
        attendance.location_out = location
        attendance.save()
        action = 'out'
    else:
        action = 'in'

    return JsonResponse({'status': 'success', 'action': action})

@login_required
def employee_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user.employee
            leave.status = 'PENDING'
            leave.save()
            return redirect('employee_leave_history')
    else:
        form = LeaveRequestForm()

    context = {
        'form': form,
    }
    return render(request, 'leave_request.html', context)

@login_required
def employee_leave_history(request):
    employee = request.user.employee
    leaves = Leave.objects.filter(employee=employee).order_by('-start_date')
    context = {
        'leaves': leaves,
    }
    return render(request, 'leave_history.html', context)

@login_required
def employee_payslips(request):
    employee = request.user.employee
    payslips = Payslip.objects.filter(employee=employee).order_by('-month')
    context = {
        'payslips': payslips,
    }
    return render(request, 'payslips.html', context)

@login_required
def employee_performance(request):
    employee = request.user.employee
    reviews = PerformanceReview.objects.filter(employee=employee).order_by('-review_date')
    context = {
        'reviews': reviews,
    }
    return render(request, 'performance.html', context)

@login_required
def employee_salary_info(request):
    employee = request.user.employee
    salary = Salary.objects.filter(employee=employee).first()
    context = {
        'salary': salary,
    }
    return render(request, 'salary_info.html', context)

@login_required
def employee_notifications(request):
    notices = Notice.objects.all().order_by('-date_posted')[:10]  # Get last 10 notices
    context = {
        'notices': notices,
    }
    return render(request, 'notifications.html', context)

@login_required
def employee_team(request):
    employee = request.user.employee
    team_members = Employee.objects.filter(department=employee.department).exclude(id=employee.id)
    context = {
        'department': employee.department,
        'team_members': team_members,
    }
    return render(request, 'team.html', context)