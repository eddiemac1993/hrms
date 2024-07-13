from django.contrib import admin
from django.urls import path, include  # Import include to include app urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hrms.urls')),  # Include app urls
]
