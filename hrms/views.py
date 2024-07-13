from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import HttpResponse
from .forms import UserRegistrationForm, EmployeeProfileForm, AttendanceForm, LeaveForm, PerformanceReviewForm, NoticeForm
from .models import User, Employee, Attendance, Leave, PerformanceReview, Notice, Department

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
