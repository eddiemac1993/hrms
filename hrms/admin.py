from django.contrib import admin
from .models import User, Department, Employee, Attendance, Salary, Payslip, PerformanceReview, Leave, Notice

# Register your models here
admin.site.register(User)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Salary)
admin.site.register(Payslip)
admin.site.register(PerformanceReview)
admin.site.register(Leave)
admin.site.register(Notice)
