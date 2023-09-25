# Generated by Django 4.0.4 on 2023-09-25 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_app', '0002_rename_sex_profile_gender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientID', models.PositiveIntegerField()),
                ('consultantID', models.PositiveIntegerField()),
                ('clientName', models.CharField(max_length=40, null=True)),
                ('consultantName', models.CharField(max_length=40, null=True)),
                ('category', models.CharField(choices=[('Dating', 'Dating'), ('Relationships', 'Relationships'), ('Breakups', 'Breakups'), ('Divorce', 'Divorce'), ('Marriage', 'Marriage'), ('Family', 'Family'), ('Business', 'Business')], max_length=100, null=True)),
                ('appointmentDate', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('requestsnotes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='consultant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=False)),
                ('assignedConsultantID', models.PositiveIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
