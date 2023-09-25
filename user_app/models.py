from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .validators import validate_file_size

def user_directory_path(instance, filename):
    return 'user_images/{0}/{1}'.format(instance.user.username, filename)

class Profile(models.Model):
    class GenderOptions(models.TextChoices):
        MALE = 'M', ('Male')
        FEMALE = 'F', ('Female')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    profile_pic = models.ImageField(default='ava.jpg', upload_to=user_directory_path, blank=True, validators=[validate_file_size])
    profileCover = models.ImageField(default='banner.jpg', upload_to=user_directory_path, blank=True, validators=[validate_file_size])
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GenderOptions.choices, blank=True, null=True) 
    seeking = models.CharField(max_length=1, choices=GenderOptions.choices, blank=True, null=True) 
    about = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    online_status = models.BooleanField(null=True, blank=True, default=False)
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
        
        img = Image.open(self.profileCover.path)

        if img.height > 1200 or img.width > 1200:
            output_size = (1200, 1200)
            img.thumbnail(output_size)
            img.save(self.profileCover.path)




class Consultant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='consultant')
    email = models.EmailField(max_length=200, null=True, blank=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
    



class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='client_DATING')
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
    