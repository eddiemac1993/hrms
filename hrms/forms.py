from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employee, Attendance, Leave, PerformanceReview, Notice, Department

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmployeeProfileForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = Employee
        fields = ['department', 'photo']

class AttendanceForm(forms.ModelForm):
    time_in = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    time_out = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    location = forms.CharField(max_length=255)

    class Meta:
        model = Attendance
        fields = ['date', 'time_in', 'time_out', 'location']

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'reason', 'document']

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ['review_date', 'rating', 'comments']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
