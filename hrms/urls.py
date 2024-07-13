from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/manage/', views.manage_employees, name='manage_employees'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/list/', views.leave_list, name='leave_list'),
    path('leaves/manage/', views.manage_leaves, name='manage_leaves'),
    path('performance/review/<int:employee_id>/', views.submit_performance_review, name='submit_performance_review'),
    path('notices/view/', views.view_notices, name='view_notices'),
    path('notices/post/', views.post_notice, name='post_notice'),
]
