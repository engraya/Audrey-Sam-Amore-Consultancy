from django.contrib import admin
from .models import Consultant, ConsultancyCategories, Client, ConsultancyService, Appointment, ConsultationRequest, Message, Notification, ClientDischargeDetails, ClientPrescription
# Register your models here.

admin.site.register(ConsultationRequest)
admin.site.register(ConsultancyService)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(ConsultancyCategories)




#..........................New Registers...................#


# Register your models here.
class ConsultantAdmin(admin.ModelAdmin):
    pass
admin.site.register(Consultant, ConsultantAdmin)

class ClientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, ClientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class CientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClientDischargeDetails, CientDischargeDetailsAdmin)
admin.site.register(ClientPrescription)