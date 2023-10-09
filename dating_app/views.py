from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from user_app.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Favorite, Appointment, Client, Message
from .forms import MessageForm, AppointmentForm, ClientMessageForm
import random


@login_required
def dating(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.about:
		query = request.GET.get("q", default = "")
		gender = request.GET.get('gender', default = "ALL")
		if gender == 'ALL':
			gender = ['M', 'F']
		
		profiles_list = Profile.objects.filter(
				Q(first_name__icontains=query) | Q(last_name__icontains=query), gender__in=gender
			).exclude(id=request.user.id)

		context = get_pogination(request, profiles_list, 10)
		if profiles_list:
			context.update({'query': f'We found {len(profiles_list)} people with name "{query}"'})
			context.update({'saved_to_favorite': Favorite.objects.values_list('saved', flat=True)})
			context.update({'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')})
		else:
			context.update({'query': f'There are no people with name "{query}"'})
		return render(request, 'dating.html', context)
	return redirect('user_app:sign_up_step_three')


def favorite_add(request, user_id):
	saved = User.objects.get(id=user_id)
	favorites = Favorite.objects.filter(user=request.user, saved=saved)

	if not favorites.exists():
		Favorite.objects.create(user=request.user, saved=saved)
	else:
		favorite = favorites.first()
		favorite.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])




@login_required
def partner_account(request, user_id):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.about:
		
		partner_account = get_object_or_404(User, pk=user_id)
		return render(request, 'partner_account.html', {'partner_account':partner_account, 'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')})
	return redirect('user_app:sign_up_step_three')

@login_required
def home(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.about:
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


def random_card(request):
	profile = Profile.objects.get(pk=request.user.pk)
	card_list = list(Profile.objects.filter(gender__in=str(profile.seeking)
			).exclude(id=request.user.id))
	if card_list:
		random_card = random.sample(card_list, 1)
	else:
		random_card = None
	return render(request, 'random_card.html', {'random_card':random_card, 'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')})


#-----------------ADMIN VIEWS STARTS----------------------------------------------------------------#####


def adminPage(request):
	return render(request, 'adminPage.html')



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
	return render(request, 'adminPage.html', context)


#-----------------APPOINTMENT START----------------------------------------------------------------#####

def admin_appointment_view(request):
    return render(request,'admin_appointment.html')


def admin_view_appointment_view(request):
    appointments = Appointment.objects.all()
    context = {'appointments':appointments}
    return render(request,'admin_view_appointment.html', context)


def admin_appointment_history_view(request):
	appointments = Appointment.objects.all()
	context = {'appointments' : appointments}
	return render(request, 'admin_appointment_history.html', context)


def admin_approve_appointment_view(request):
    appointments = Appointment.objects.all().filter(status=False)
    context = {'appointments':appointments}
    return render(request,'admin_approve_appointment.html', context)


def approve_appointment(request, pk):
	appointment = Appointment.objects.get(id=pk)
	appointment.status=True
	appointment.save()
	return redirect('dating_app:admin-approve-appointment')


def reject_appointment(request, pk):
	appointment = Appointment.objects.get(id=pk)
	appointment.delete()
	return redirect('dating_app:admin-approve-appointment')


#-----------------MESSAGES START----------------------------------------------------------------#####

def admin_messages_view(request):
    return render(request,'admin_messages.html')


def admin_view_messages_view(request):
	messages = Message.objects.filter(sender__groups__name='CLIENT')
	context = {'messages' : messages}
	return render(request, 'admin_view_messages.html', context)



def admin_read_messages_view(request):
    messages = Message.objects.filter(sender__groups__name='CLIENT')
    context = {'messages':messages}
    return render(request,'admin_read_messages.html', context)


def admin_outbox(request):
	messages = Message.objects.filter(sender=request.user)
	context = {'messages' : messages}
	return render(request, 'admin_outbox.html', context)


def read_messages(request, pk):
	message = Message.objects.get(id=pk)
	message.status=True
	message.save()
	return redirect('dating_app:admin-read-messages')


def reject_messages(request, pk):
	message = Message.objects.get(id=pk)
	message.delete()
	return redirect('dating_app:admin-read-messages')


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

def admin_reply_messages_view(request):
	return render(request, 'admin_reply_messages.html')


#-----------------MESSAGES END----------------------------------------------------------------#####


def admin_client_view(request):
    return render(request,'admin_client.html')



def admin_view_client_view(request):
	clientGroup = Group.objects.get(name="CLIENT")
	clientUsers = clientGroup.user_set.all()
	context = {'clients' : clientUsers}
	return render(request, 'admin_view_client.html', context)

def delete_client_view(request,pk):
    client= Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-view-client')

#-----------------CLIENT VIEW STARTS HERE----------------------------------------------------------------#####


def client_dashboard_view(request):
	appointments = Appointment.objects.all().filter(clientID=request.user.id)
	messages = Message.objects.all().filter(senderID=request.user.id)
	appointmentcount = Appointment.objects.all().filter(status=True).count()
	pendingappointmentcount = Appointment.objects.all().filter(status=False)
	messagescount = Message.objects.all().filter(status=True).count()
	pendingmessagescount = Message.objects.all().filter(status=False).count()

	context = {
		'appointmentcount':appointmentcount,
		'pendingappointmentcount':pendingappointmentcount,
		'messagescount':messagescount,
		'pendingmesssagescount':pendingmessagescount,
		'appointments' : appointments,
		'messages' : messages
	}
	return render(request, 'client_dashboard.html', context)


def client_appointment_view(request):
    return render(request,'client_appointment.html')


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
		


def client_cancel_appointment_view(request, pk):
	appointment = Appointment.objects.get(id=pk)
	appointment.delete()
	return redirect('dating_app:client-appointment-history')

def client_view_appointment_view(request):
	appointments = Appointment.objects.all().filter(clientID=request.user.id)
	context = {'appointments' : appointments}
	return render(request, 'client_view_appointment.html', context)



def client_appointment_history(request):
	appointments = Appointment.objects.filter(status=False)
	context = {'appointments' : appointments}
	return render(request, 'client_appointment_history.html', context)	


#-----------------MESSAGES START----------------------------------------------------------------#####

def client_messages_view(request):
	return render(request, 'client_messages.html')


def client_view_messages_view(request):
	messages = Message.objects.all().filter(senderID=request.user.id)
	context = {'messages' : messages}
	return render(request, 'client_view_messages.html', context)



def client_read_messages_view(request):
    messages = Message.objects.all().filter(status=False)
    context = {'messages':messages}
    return render(request,'client_read_messages.html', context)


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

def client_messages_outbox(request):
	messages = Message.objects.filter(sender=request.user)
	context = {'messages' : messages}
	return render(request, 'client_outbox.html', context)


def client_delete_messages(request, pk):
	message = Message.objects.get(id=pk)
	message.delete()
	return redirect('dating_app:client-outbox')




def send_message(request, recipient_id):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.sender = request.user
			message.recipient_id = recipient_id
			message.save()
			return redirect('client-dashboard')
		else:
			form = MessageForm()
	context = {'form' : form}
	return render(request, 'send_message.html', context)




def schedule_appointment(request, admin_id):
	if request.method == 'POST':
		form = AppointmentForm(request.POST)
		if form.is_valid():
			appointment = form.save(commit=False)
			appointment.client = request.user
			appointment.admin_id = admin_id
			appointment.save()
			return redirect('client-dashboard')
		else:
			form = AppointmentForm()
	context = {'form' : form}
	return render(request, 'schedule_appointment', context)


def message_list(request):
	messages = Message.objects.filter(recipient=request.user)
	context = {'messages' : messages}
	return render(request, 'message.html', context)


def appointment_list(request):
	appointments = Appointment.objects.filter(client=request.user)
	context = {'appointments' : appointments}
	return render(request, 'appointment_list.html', context)