from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DutyStation, Department, Employee, Attendance, Payslip, PerformanceReview, Leave, Notice

admin.site.site_header = "Human Resource Management System"

# admin.py
from django.contrib import admin
from .models import CentralLocation

admin.site.register(CentralLocation)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'duty_station')
    list_filter = ('is_staff', 'is_admin', 'duty_station')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_admin', 'duty_station')}),
    )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'duty_station')
    list_filter = ('duty_station',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'duty_station')
    list_filter = ('department', 'duty_station')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'time_in', 'time_out')
    list_filter = ('date', 'employee__department', 'employee__duty_station')
    search_fields = ('employee__user__username',)

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'amount')
    list_filter = ('employee__department', 'employee__duty_station')
    search_fields = ('employee__user__username',)

class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'amount')
    list_filter = ('month', 'employee__department', 'employee__duty_station')
    search_fields = ('employee__user__username',)

class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_date', 'rating')
    list_filter = ('review_date', 'rating', 'employee__department', 'employee__duty_station')
    search_fields = ('employee__user__username',)

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'employee__department', 'employee__duty_station')
    search_fields = ('employee__user__username',)

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'duty_station')
    list_filter = ('date_posted', 'duty_station')
    search_fields = ('title', 'content')

admin.site.register(User, CustomUserAdmin)
admin.site.register(DutyStation)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Payslip, PayslipAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(Notice, NoticeAdmin)
