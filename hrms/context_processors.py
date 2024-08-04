from .models import User

def duty_station(request):
    if request.user.is_authenticated:
        return {
            'duty_station': request.user.duty_station,
        }
    return {}
