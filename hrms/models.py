# hrms/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from geopy.distance import distance

class DutyStation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CentralLocation(models.Model):
    duty_station = models.OneToOneField(DutyStation, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Central Location for {self.duty_station}"

class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    duty_station = models.ForeignKey(DutyStation, on_delete=models.SET_NULL, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name='hrms_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='hrms_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.get_full_name()

class Department(models.Model):
    name = models.CharField(max_length=100)
    duty_station = models.ForeignKey(DutyStation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    duty_station = models.ForeignKey(DutyStation, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()

    def full_name(self):
        return self.user.get_full_name()

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    location_in = models.CharField(max_length=255, null=True, blank=True)
    location_out = models.CharField(max_length=255, null=True, blank=True)
    distance_in = models.FloatField(null=True, blank=True)
    distance_out = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.time_in = timezone.now()
            self.location_in = self.location_in if self.location_in else "Default Location In"
            self.calculate_distance_in()
        else:
            self.time_out = timezone.now()
            self.location_out = self.location_out if self.location_out else "Default Location Out"
            self.calculate_distance_out()
        super().save(*args, **kwargs)

    def calculate_distance_in(self):
        if self.location_in and self.employee.duty_station:
            central_location = CentralLocation.objects.get(duty_station=self.employee.duty_station)
            self.distance_in = self.calculate_distance(
                central_location.latitude,
                central_location.longitude,
                *self.parse_location(self.location_in)
            )

    def calculate_distance_out(self):
        if self.location_out and self.employee.duty_station:
            central_location = CentralLocation.objects.get(duty_station=self.employee.duty_station)
            self.distance_out = self.calculate_distance(
                central_location.latitude,
                central_location.longitude,
                *self.parse_location(self.location_out)
            )

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        return distance((lat1, lon1), (lat2, lon2)).kilometers

    @staticmethod
    def parse_location(location_str):
        lat, lon = map(float, location_str.split(','))
        return lat, lon

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
    duty_station = models.ForeignKey(DutyStation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
