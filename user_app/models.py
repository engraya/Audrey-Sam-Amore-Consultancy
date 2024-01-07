from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .validators import validate_file_size
from django_countries.fields import CountryField

def user_directory_path(instance, filename):
    return 'user_images/{0}/{1}'.format(instance.user.username, filename)


RelationshipStatus_CHOICES = [('Never Married', 'Never Married'), 
                 ('Divorced', 'Dovorced'),
                 ('Seperated', 'Seperated'),
                 ('Widowed', 'Widowed'),
                 ('Married', 'Married'),
                 ('Seeking for Partner', 'Seeking for Partner')
                 ]
KidsStatus_CHOICES = [('No', 'No'),
              ('Yes', 'Yes'),
              ('Undecided', 'Undecided')
              ]

PartnerPreference_CHOICES = [('No Preference', 'No Preference'),
                     ('White/Caucasian', 'White/Caucasian'),
                     ('Black/African', 'Black/African'),
                     ('Asian', 'Asian'),
                     ('Latin/Hispanic', 'Latin/Hispanic'),
                     ('Indian', 'Indian'),
                     ('Middle Eastern', 'Middle Eastern'),
                     ('Native American', 'Native American'),
                     ('Mixed', 'Mixed'),
                     ('Other', 'Other')
                     ]

Complexion_CHOICES = [('Dark', 'Dark'),
              ('Chocolate', 'Chocolate'),
              ('Fair', 'Fair'),
              ('White', 'White')
              ]

SeekingRelationship_CHOICES = [('Starting Family', 'Starting Family'),
                       ('Marriage', 'Marriage'),
                       ('Long Term', 'Long Term'),
                       ('Short Term', 'Short Term'),
                       ('Emotional Connection', 'Emotional Connection'),
                       ('Companionship', 'Companionship'),
                       ('Mentor', 'Mentor')
                       ]
class Profile(models.Model):
    class GenderOptions(models.TextChoices):
        MALE = 'M', ('Male')
        FEMALE = 'F', ('Female')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    profile_pic = models.ImageField(default='clear.png', upload_to=user_directory_path, blank=True, validators=[validate_file_size])
    age = models.PositiveIntegerField(null=True, blank=True)
    relationshipStatus = models.CharField(max_length=20, choices=RelationshipStatus_CHOICES, blank=True, null=True)
    kidsStatus = models.CharField(max_length=20, choices=KidsStatus_CHOICES, null=True, blank=True)
    hobbyList = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)
    partnerPreference = models.CharField(max_length=20, choices=PartnerPreference_CHOICES, null=True, blank=True)
    complexion = models.CharField(max_length=20, choices=Complexion_CHOICES, null=True, blank=True)
    seekingRelationship = models.CharField(max_length=20, choices=SeekingRelationship_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GenderOptions.choices, blank=True, null=True) 
    seeking = models.CharField(max_length=1, choices=GenderOptions.choices, blank=True, null=True) 
    about = models.TextField(null=True, blank=True)
    country = CountryField(blank_label="Select Country", null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True, choices=CountryField().choices, blank_label="Select Country")
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
        
        # img = Image.open(self.profileCover.path)

        # if img.height > 1200 or img.width > 1200:
        #     output_size = (1200, 1200)
        #     img.thumbnail(output_size)
        #     img.save(self.profileCover.path)

    
