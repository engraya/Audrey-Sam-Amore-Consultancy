from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UserUpdateForm, ProfileUpdateForm, SignUpStepOneForm, SignUpStepTwoForm, SignUpStepThreeForm, AdminRegistrationForm, AdminLoginForm, ClientLoginForm, ClientRegistrationForm
from .models import Profile
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib import messages
from dating_app.models import Message, Appointment


def corePage(request):
	return render(request, 'corePage.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'adminClick.html')


#for showing signup/login button for doctor(by sumit)
def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'clientClick.html')




def admin_signup(request):
	error_contex = []
	if request.method == 'GET':
		context = {'form': AdminRegistrationForm}
		return render(request, 'admin_sign_up.html', context)
	else:
		try:
			user = User.objects.create_user(username = request.POST['username'], password=request.POST['password'])
			user.save()
			my_admin_group = Group.objects.get_or_create(name='ADMIN')
			my_admin_group[0].user_set.add(user)
			login(request, user)
			return redirect('user_app:admin_sign_in')
		except IntegrityError:
			error_contex.append('That username has already been taken')
			return render(request, 'admin_sign_up.html', {'form': AdminRegistrationForm(), 'error_contex': error_contex})	
	return render(request, 'user_app/admin_sign_up.html', {'form': AdminRegistrationForm(), 'error_contex': error_contex})



def client_signup(request):
	if request.method == 'POST':
		form = ClientRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data.get('password'))
			user.save()
			my_client_group = Group.objects.get_or_create(name='CLIENT')
			my_client_group[0].user_set.add(user)
			login(request, user)
			return redirect('user_app:sign_up_step_one')
	else:
		form = ClientRegistrationForm()	
		context = {'form': form}
		return render(request, 'sign_up.html', context)	



def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()



def afterlogin_view(request):
	if is_admin(request.user):
		return redirect('dating_app:adminPage')
	if is_client(request.user):
		return redirect('dating_app:dating')



def admin_login(request):
	if request.method == 'POST':
		form = AdminLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.groups.filter(name='ADMIN').exists():
					login(request, user)
					messages.info(request, 'You are now Loggged in as admin')
					return redirect('dating_app:adminPage')
			else:
				messages.error(request, "Invalid Username or Password, Try agin later!")
		else:
			messages.error(request, "Invalid Username or Password, Try again later!")

	form = AdminLoginForm()
	context = {'form' : form}
	return render(request, 'admin_sign_in.html', context)


def client_login(request):
	if request.method == 'POST':
		form = ClientLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.groups.filter(name='CLIENT').exists():
					login(request, user)
					messages.info(request, 'You are now Loggged in as client')
					return redirect('dating_app:clientPage')
			else:
				messages.error(request, "User Group Does not exist!, Try agin later!")
		else:
			messages.error(request, "Invalid Username or Password, Try again later!")

	form = ClientLoginForm()
	context = {'form' : form}
	return render(request, 'client_sign_in.html', context)


		



@login_required
def logout_user(request):
	if request.method == 'POST':
		logout(request)
		return redirect('/')


@login_required
def user_account(request):
	appointmentCount = Appointment.objects.all().filter(client=request.user, status=True).count()
	messageCount = Message.objects.all().filter(senderID=request.user.id, status=True).count()
	pendingAppointments = Appointment.objects.all().filter(client=request.user, status=False).count()
	pendingMessages = Message.objects.all().filter(sender=request.user, recipient=request.user, status=False).count()


	profile = Profile.objects.get_or_create(user_id=request.user.id)
	if request.user.profile.about:
		if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=request.user)
			p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
			if u_form.is_valid() &  p_form.is_valid():
				u_form.save()
				p_form.save()
			return redirect('user_app:user_account') 
		else:
			u_form = UserUpdateForm(instance=request.user)
			p_form = ProfileUpdateForm(instance=request.user.profile)

		context = {
			'u_form': u_form,
			'p_form': p_form,
			'profile' : profile,
			'totalAppointments' : appointmentCount,
			'totalMessages' : messageCount,
			'pendingAppointments' : pendingAppointments,
			'pendingMesssages' : pendingMessages
		}

		return render(request, 'user_account.html', context)
	
	return redirect('user_app:sign_up_step_three')


@login_required
def sign_up_step_one(request):
	if request.method == 'POST':
		step_one_form = SignUpStepOneForm(request.POST,request.FILES,instance=request.user.profile)
		if step_one_form.is_valid():
			step_one_form.save()
			
		return redirect('user_app:sign_up_step_two')
	else:
		step_one_form = SignUpStepOneForm()

	context = {
		'form': step_one_form,
	}
	return render(request, 'sign_up_step_one.html', context)



@login_required
def sign_up_step_two(request):
	profile = Profile.objects.get(user_id=request.user.id)
	if profile.relationshipStatus and profile.age:
		if request.method == 'POST':
			step_two_form = SignUpStepTwoForm(request.POST,request.FILES,instance=profile)
			if step_two_form.is_valid():
				step_two_form.save()
				profile.user = request.user
				profile.save()
			return redirect('user_app:sign_up_step_three')
		else:
			step_two_form = SignUpStepTwoForm()

		context = {
			'form': step_two_form,
		}
		return render(request, 'sign_up_step_two.html', context)
	return redirect('user_app:sign_up_step_one')


@login_required
def sign_up_step_three(request):
	profile = Profile.objects.get(user_id=request.user.id)
	if profile.city and profile.country and profile.state and profile.kidsStatus and profile.partnerPreference and profile.complexion and profile.seekingRelationship:
		if request.method == 'POST':
			step_three_form = SignUpStepThreeForm(request.POST,request.FILES,instance=request.user.profile)
			if not(request.POST['about']):
				return render(request, 'user_app/sign_up_step_three.html', {'error': 'About field can\'t be empty'})
			else:
				try:
					step_three_form.save()
					return redirect('dating_app:dating')
				except ValueError:
					return render(request, 'user_app/sign_up_step_three.html', {'error': 'File is too large, requirement is less than 2.5 MB'})
		else:
			step_three_form = SignUpStepThreeForm(instance=request.user.profile)

		context = {
			'form': step_three_form,
		}
		return render(request, 'sign_up_step_three.html', context)
	return redirect('user_app:sign_up_step_two')




