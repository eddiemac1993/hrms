from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name='hrms_user_set',  # Custom related name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='hrms_user_set',  # Custom related name
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField(null=True, blank=True)
    location_in = models.CharField(max_length=255)
    location_out = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.id:
            # Only set time_in automatically on creation
            self.time_in = timezone.now().time()
        super().save(*args, **kwargs)

class Salary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee} - {self.amount}"

class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee} - {self.month}"

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_date = models.DateField()
    rating = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.review_date}"

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ])
    document = models.FileField(upload_to='leave_documents/', null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
