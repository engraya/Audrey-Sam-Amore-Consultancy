from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UserUpdateForm, ProfileUpdateForm, SignUpStepOneForm, SignUpStepTwoForm, SignUpStepThreeForm, AdminRegistrationForm, AdminLoginForm, ClientLoginForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from dating_app.models import Favorite
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib import messages


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
	error_contex = []
	if request.method == 'GET':
		context = {'form': UserCreationForm}
		return render(request, 'sign_up.html', context)
	else:
		if not(request.POST['username']):
			error_contex.append('Login can\'t be empty')
		elif not(request.POST['password1']):
			error_contex.append('Password can\'t be empty')
		elif not(request.POST['password2']):
			error_contex.append('Confirm Password can\'t be empty')
		elif request.POST['password1'] != request.POST['password2']:
			error_contex.append('Password did not match')
		elif len(request.POST['password1']) < 8:
			error_contex.append('Password less then 8 characters')
		elif str(request.POST['username']).lower() in ['admin', 'админ', 'аdmin', 'god', 'administrator', 'аdministrator', 'аdministrаtor']:
			error_contex.append('This login can\'t be taken')
		else:
			try:
				user = User.objects.create_user(username = request.POST['username'], password=request.POST['password1'])
				user.save()
				my_client_group = Group.objects.get_or_create(name='CLIENT')
				my_client_group[0].user_set.add(user)
				if user is not None:
					if user.groups.filter(name='CLIENT').exists():
						login(request, user)
						return redirect('user_app:sign_up_step_one')
			except IntegrityError:
				error_contex.append('That username has already been taken')
				return render(request, 'sign_up.html', {'form': UserCreationForm(), 'error_contex': error_contex})	
		return render(request, 'user_app/sign_up.html', {'form': UserCreationForm(), 'error_contex': error_contex})




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()



def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('dating:adminPage')
    elif is_client(request.user):
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
					messages.info(request, 'You are now Loggged in as admin')
					return redirect('dating_app:dating')
			else:
				messages.error(request, "Invalid Username or Password, Try agin later!")
		else:
			messages.error(request, "Invalid Username or Password, Try again later!")

	form = ClientLoginForm()
	context = {'form' : form}
	return render(request, 'sign_in.html', context)


		



@login_required
def logout_user(request):
	if request.method == 'POST':
		logout(request)
		return redirect('/')


@login_required
def user_account(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.about:
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
		}

		return render(request, 'user_account.html', context)
	
	return redirect('user_app:sign_up_step_three')


@login_required
def sign_up_step_one(request):
	if request.method == 'POST':
		step_one_form = SignUpStepOneForm(request.POST,
									request.FILES,
									instance=request.user.profile)
		if not(request.POST['first_name']):
			return render(request, 'sign_up_step_one.html', {'error': 'First name can\'t be empty'})
		if not(str(request.POST['first_name']).isalpha()):
			return render(request, 'sign_up_step_one.html', {'error': 'First name can\'t have numbers'})
		elif not(request.POST['last_name']):
			return render(request, 'sign_up_step_one.html', {'error': 'Last name can\'t be empty'})
		if not(str(request.POST['last_name']).isalpha()):
			return render(request, 'sign_up_step_one.html', {'error': 'Last name can\'t have numbers'})
		elif not(request.POST['age']):
			return render(request, 'sign_up_step_one.html', {'error': 'Age can\'t be empty'})
		elif int(request.POST['age']) < 18:
			return render(request, 'user_app/sign_up_step_one.html', {'error': 'Your age must be at least 18 years old'})
		elif not str(request.POST['age']).isnumeric():
				return render(request, 'sign_up_step_one.html', {'error':'Uncorrect age field'})
		else:
			step_one_form.save()
			return redirect('user_app:sign_up_step_two')
	else:
		step_one_form = SignUpStepOneForm(instance=request.user.profile)

	context = {
		'step_one_form': step_one_form,
	}
	return render(request, 'sign_up_step_one.html', context)



@login_required
def sign_up_step_two(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.first_name and profile.last_name and profile.age:
		if request.method == 'POST':
			step_two_form = SignUpStepTwoForm(request.POST,
										request.FILES,
										instance=request.user.profile)
			if not(request.POST['city']):
				return render(request, 'sign_up_step_two.html', {'error': 'Location can\'t be empty'})
			elif request.POST['gender'] not in ['M', 'F']:
					return render(request, 'sign_up_step_two.html', {'error': 'Choose correct gender field'})
			elif request.POST['seeking'] not in ['M', 'F']:
					return render(request, 'sign_up_step_two.html', {'error': 'Choose correct seeking field'})
			else:
				step_two_form.save()
				return redirect('user_app:sign_up_step_three')
		else:
			step_two_form = SignUpStepTwoForm(instance=request.user.profile)

		context = {
			'step_two_form': step_two_form,
		}
		return render(request, 'sign_up_step_two.html', context)
	return redirect('user_app:sign_up_step_one')


@login_required
def sign_up_step_three(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.city and profile.gender and profile.seeking:
		if request.method == 'POST':
			step_three_form = SignUpStepThreeForm(request.POST,
										request.FILES,
										instance=request.user.profile)
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
			'step_three_form': step_three_form,
		}
		return render(request, 'sign_up_step_three.html', context)
	return redirect('user_app:sign_up_step_two')




