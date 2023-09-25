from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_app.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Favorite, Appointment, Client
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


def adminPage(request):
	return render(request, 'adminPage.html')


def admin_dashboard_view(request):
    clients = User.objects.all().order_by('-id')
    clientcount = User.objects.all().count()
    appointmentcount = Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = Appointment.objects.all().filter(status=False).count()

    context = {
    'clients':clients,
    'clientcount':clientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'adminPage.html',context)

#-----------------APPOINTMENT START----------------------------------------------------------------#####

def admin_appointment_view(request):
    return render(request,'admin_appointment.html')



def admin_view_appointment_view(request):
    appointments = Appointment.objects.all().filter(status=True)
    context = {'appointments':appointments}
    return render(request,'admin_view_appointment.html', context)



def admin_approve_appointment_view(request):
    appointments = Appointment.objects.all().filter(status=False)
    context = {'appointments':appointments}
    return render(request,'admin_approve_appointment.html', context)




def approve_appointment_view(request,pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect('admin-approve-appointment')




def reject_appointment_view(request,pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')



def admin_client_view(request):
    return render(request,'admin_client.html')


def admin_view_client_view(request):
    clients = Client.objects.all().filter(status=True)
    context = {'clients':clients}
    return render(request,'admin_view_client.html', context)


def delete_client_view(request,pk):
    client= Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-view-client')
