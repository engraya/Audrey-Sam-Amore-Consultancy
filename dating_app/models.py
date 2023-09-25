from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	saved = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
	saved_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f'Пользователь {self.user} | Сохранил {self.saved}'
	


APPOINTMENT_REQUEST_CATEGORY=[('Dating','Dating'),
('Relationships','Relationships'),
('Breakups','Breakups'),
('Divorce','Divorce'),
('Marriage','Marriage'),
('Family','Family'),
('Business','Business'),
]
class Appointment(models.Model):
    clientID=models.PositiveIntegerField(null=False)
    consultantID=models.PositiveIntegerField(null=False)
    clientName=models.CharField(max_length=40,null=True)
    consultantName=models.CharField(max_length=40,null=True)
    category = models.CharField(max_length=100, choices=APPOINTMENT_REQUEST_CATEGORY, null=True)
    appointmentDate=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    requestsnotes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category
    


class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='client')
    email = models.EmailField(max_length=200, null=True, blank=True)
    status=models.BooleanField(default=False)
    assignedConsultantID = models.PositiveIntegerField(null=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
    