from .models import MainAppointment

'''This  module was introduce to inject a particular data'''

def get_notification(request):
    count = MainAppointment.objects.filter(accepted=False).count()

    # the injected data
    data = {
        'count': count,
    }
    return data