from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from user_app.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Appointment, Client, Message
from .forms import MessageForm, AppointmentForm, ClientMessageForm
import random


@login_required
def dating(request):
	profile = Profile.objects.get(user_id=request.user.id)
	if profile:
		query = request.GET.get("q", default = "")
		gender = request.GET.get('gender', default = "ALL")
		if gender == 'ALL':
			gender = ['M', 'F']
		
		# profiles_list = Profile.objects.filter(
		# 		Q(first_name__icontains=query) | Q(last_name__icontains=query), gender__in=gender
		# ).exclude(user_id=request.user.id)

		clientGroup = Group.objects.get(name='CLIENT')
		profiles_list = Profile.objects.filter(user__groups=clientGroup).exclude(user_id=request.user.id)

		context = get_pogination(request, profiles_list, 10)
		return render(request, 'dating.html', context)
	return redirect('user_app:sign_up_step_three')


@login_required
def partner_account(request, user_id):
	# profile = Profile.objects.get(pk=user_id)
	clientGroup = Group.objects.get(name='CLIENT')
	profile = Profile.objects.filter(user__groups=clientGroup).get(pk=user_id)
	if profile.about:

		partner_account = get_object_or_404(User, pk=user_id)
		context = {'partner_account':partner_account, 'profile' : profile}
		return render(request, 'partner_account.html', context)
	return redirect('user_app:sign_up_step_three')

@login_required
def home(request):
	profile = Profile.objects.get_or_create(user_id=request.user.id)
	if profile:
		return redirect('dating_app:dating')
	return redirect('user_app:sign_up_step_three')



def get_pogination(request, profiles_list, objects_num):
	paginator = Paginator(profiles_list, objects_num)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	
	try:
		cards = paginator.page(page)
	except(EmptyPage, InvalidPage):
		cards = paginator.page(paginator.num_pages)
	page_range = paginator.get_elided_page_range(number=page)

	context = {
		'cards':cards,
		'page_range': page_range
	}
	return context


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()


#-----------------ADMIN VIEWS STARTS----------------------------------------------------------------#####

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def adminPage(request):
	return render(request, 'admin_dashboard.html')
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
	clients = Client.objects.all().count()
	appointmentcount = Appointment.objects.all().filter(status=True).count()
	pendingappointmentcount = Appointment.objects.all().filter(status=False).count()
	messagescount = Message.objects.all().filter(status=True).count()
	pendingmessagescount = Message.objects.all().filter(status=False).count()
	userscount = User.objects.all().count

	clientsGroup = Group.objects.get(name="CLIENT")
	clientUsers = clientsGroup.user_set.all()
	clientsUsersCount = clientUsers.count()

	context = {
		'clients':clients,
		'messagescount':messagescount,
		'pendingmessagescount':pendingmessagescount,
		'appointmentcount':appointmentcount,
		'pendingappointmentcount':pendingappointmentcount,
		'userscount' : userscount,
		'clientUsersCount' : clientsUsersCount
	}
	return render(request, 'admin_dashboard.html', context)


	
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_client_view(request):
    return render(request,'admin_client.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_client_view(request):
	clientGroup = Group.objects.get(name="CLIENT")
	clientUsers = clientGroup.user_set.all()
	context = {'clients' : clientUsers}
	return render(request, 'admin_view_client.html', context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_client_view(request,pk):
    client= Client.objects.get(id=pk)
    user = User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-view-client')

#-----------------ADMIN APPOINTMENT STARTS HERE----------------------------------------------------------------#####
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = Appointment.objects.all()
    context = {'appointments':appointments}
    return render(request,'admin_view_appointment.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_history_view(request):
	appointments = Appointment.objects.all()
	context = {'appointments' : appointments}
	return render(request, 'admin_appointment_history.html', context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    appointments = Appointment.objects.all().filter(status=False)
    context = {'appointments':appointments}
    return render(request,'admin_approve_appointment.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment(request, pk):
	appointment = Appointment.objects.get(id=pk)
	appointment.status=True
	appointment.save()
	return redirect('dating_app:admin-approve-appointment')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment(request, pk):
	appointment = Appointment.objects.get(id=pk)
	appointment.delete()
	return redirect('dating_app:admin-approve-appointment')

#-----------------ADMIN APPOINTMENTS ENDS HERE----------------------------------------------------------------#####



#-----------------AMIN MESSAGES STARTS HERE----------------------------------------------------------------#####
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_messages_view(request):
    return render(request,'admin_messages.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_messages_view(request):
	messages = Message.objects.filter(sender__groups__name='CLIENT')
	context = {'messages' : messages}
	return render(request, 'admin_view_messages.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_read_messages_view(request):
    messages = Message.objects.filter(sender__groups__name='CLIENT')
    context = {'messages':messages}
    return render(request,'admin_read_messages.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_outbox(request):
	messages = Message.objects.filter(sender=request.user)
	context = {'messages' : messages}
	return render(request, 'admin_outbox.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def read_messages(request, pk):
	message = Message.objects.get(id=pk)
	message.status=True
	message.save()
	return redirect('dating_app:admin-read-messages')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_messages(request, pk):
	message = Message.objects.get(id=pk)
	message.delete()
	return redirect('dating_app:admin-read-messages')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_send_messages_view(request):
	messageForm = MessageForm()
	if request.method == 'POST':
		messageForm = MessageForm(request.POST)
		if messageForm.is_valid():
			message = messageForm.save(commit=False)
			message.senderID = request.user.id
			message.senderName = request.user.first_name
			message.content = request.POST.get('content')
			message.sender = request.user
			message.status = False
			message.save()
			return redirect('dating_app:admin-outbox')
	context = {'form' : messageForm}
	return render(request, 'admin_send_messages.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_reply_messages_view(request):
	return render(request, 'admin_reply_messages.html')


#-----------------ADMIN MESSAGES ENDS HERE----------------------------------------------------------------#####




#-----------------CLIENT VIEW STARTS HERE----------------------------------------------------------------#####


@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def clientPage(request):
	return render(request, 'client_dashboard.html')

@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_dashboard_view(request):
	appointments = Appointment.objects.all().filter(clientID=request.user.id)
	messages = Message.objects.all().filter(senderID=request.user.id)
	appointmentcount = Appointment.objects.all().filter(client=request.user, status=True).count()
	pendingappointmentcount = Appointment.objects.all().filter(client=request.user, status=False).count()
	messagescount = Message.objects.all().filter(senderID=request.user.id, status=True).count()
	pendingmessagescount = Message.objects.all().filter(sender=request.user, recipient=request.user, status=False).count()

	context = {
		'appointmentcount':appointmentcount,
		'pendingappointmentcount':pendingappointmentcount,
		'messagescount':messagescount,
		'pendingmessagescount':pendingmessagescount,
		'appointments' : appointments,
		'messages' : messages
	}
	return render(request, 'client_dashboard.html', context)


@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_appointment_view(request):
    return render(request,'client_appointment.html')


@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_book_appointment(request):
	appointmentForm = AppointmentForm()
	if request.method == 'POST':
		admin_group = Group.objects.get(name="ADMIN")
		appointmentForm = AppointmentForm(request.POST)
		if appointmentForm.is_valid():
			appointment = appointmentForm.save(commit=False)
			appointment.admin = User.objects.filter(groups=admin_group).first()
			appointment.clientID = request.user.id
			appointment.clientName = request.user.first_name
			appointment.category = request.POST.get('category')
			appointment.description = request.POST.get('description')
			appointment.client = request.user
			appointment.status = False
			appointment.save()
			return redirect('dating_app:client-appointment-history')
	context = {'form' : appointmentForm}
	return render(request, 'client_book_appointment.html', context)
		


@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_cancel_appointment_view(request, pk):
	appointment = Appointment.objects.get(id=pk)
	appointment.delete()
	return redirect('dating_app:client-appointment-history')


@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_view_appointment_view(request):
	appointments = Appointment.objects.all().filter(clientID=request.user.id)
	context = {'appointments' : appointments}
	return render(request, 'client_view_appointment.html', context)



@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_appointment_history(request):
	appointments = Appointment.objects.filter(status=False)
	context = {'appointments' : appointments}
	return render(request, 'client_appointment_history.html', context)	


#-----------------CLIENT MESSAGES STARTS HERE----------------------------------------------------------------#####

@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_messages_view(request):
	return render(request, 'client_messages.html')


@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_view_messages_view(request):
	messages = Message.objects.all().filter(sender__groups__name='ADMIN', recipient=request.user)
	context = {'messages' : messages}
	return render(request, 'client_view_messages.html', context)



@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_read_messages_view(request):
    messages = Message.objects.all().filter(sender__groups__name='ADMIN', recipient=request.user)
    context = {'messages':messages}
    return render(request,'client_read_messages.html', context)


@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_send_messages(request):
	messageForm = ClientMessageForm()
	if request.method == 'POST':
		messageForm = ClientMessageForm(request.POST)
		if messageForm.is_valid():
			message = messageForm.save(commit=False)
			message.senderID = request.user.id
			message.senderName = request.user.first_name
			message.content = request.POST.get('content')
			message.sender = request.user
			message.status = False
			message.save()
			return redirect('dating_app:client-outbox')
	context = {'form' : messageForm}
	return render(request, 'client_send_messages.html', context)


@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_messages_outbox(request):
	messages = Message.objects.filter(sender=request.user)
	context = {'messages' : messages}
	return render(request, 'client_outbox.html', context)



@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_read_messages(request, pk):
	message = Message.objects.get(id=pk)
	message.status = True
	message.save()
	return redirect('dating_app:client-read-messages')



@login_required(login_url='client_login')
@user_passes_test(is_client)
def client_delete_messages(request, pk):
	message = Message.objects.get(id=pk)
	message.delete()
	return redirect('dating_app:client-outbox')


