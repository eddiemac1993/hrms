from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Leave, Employee, Attendance, Leave, PerformanceReview, Notice, Department

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['department', 'photo']

    department = forms.ModelChoiceField(queryset=Department.objects.all())

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

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'reason', 'document']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be after the start date.")

        return cleaned_data

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


