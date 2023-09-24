from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import AdminRegistrationForm, UserLoginForm, AppointmentForm, AppointmentRequestForm, AppointmentResponseForm, MessageForm
from django.contrib.auth.decorators import login_required
from .models import *
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.contrib import messages



# Create your views here.

def homePage(request):
    categories = ConsultancyCategories.objects.all()
    context = {'categories' : categories}
    return render(request, 'consultancy/homePage.html', context)


def consultantsList(request):
    consultants = Consultant.objects.all()
    context = {'consultants' : consultants}
    return render(request, 'baseapp/consultants_list.html', context)


#---------------------------------BASE PRELOGIN VIEWS--------------------------#
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'consultancy/homePage.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'consultancy/admin/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def consultantclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'baseapp/consultantclick.html')


#for showing signup/login button for patient(by sumit)
def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'baseapp/clientclick.html')


#-------------Registration Views--------#
def admin_signup_view(request):
    form=forms.AdminRegistrationForm()
    context = {'form': form}
    if request.method=='POST':
        form=forms.AdminRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            messages.success(request, 'Registration as Admin Successful, you can now login to your account.......')
            return HttpResponseRedirect('adminlogin')
    return render(request,'consultancy/admin/adminsignup.html', context)




def consultant_signup_view(request):
    userForm=forms.ConsultantUserForm()
    consultantForm=forms.ConsultantForm()
    context = {'userForm':userForm, 'consultantForm' : consultantForm}
    if request.method=='POST':
        userForm=forms.ConsultantUserForm(request.POST)
        consultantForm=forms.ConsultantForm(request.POST,request.FILES)
        if userForm.is_valid() and consultantForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            consultant=consultantForm.save(commit=False)
            consultant.user=user
            consultant=consultant.save()
            my_consultant_group = Group.objects.get_or_create(name='CONSULTANT')
            my_consultant_group[0].user_set.add(user)
            messages.success(request, 'Registration as Consultant Successful, you can now login to your account.......')
        return HttpResponseRedirect('consultantlogin')
    return render(request,'baseapp/consultantsignup.html', context)



def client_signup_view(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    context = {'userForm' : userForm, 'clientForm' : clientForm}
    if request.method=='POST':
        userForm = forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.user=user
            client.assignedConsultantID=request.POST.get('assignedConsultantID')
            client=client.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
            messages.success(request, 'Registration as Client Successful, you can now login to your account.......')
        return HttpResponseRedirect('clientlogin')
    return render(request,'baseapp/clientsignup.html', context)





#-----------for checking user is CONSULTANT , CLIENT or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_consultant(user):
    return user.groups.filter(name='CONSULTANT').exists()
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CONSULTANT OR CLIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_consultant(request.user):
        accountapproval=models.Consultant.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('consultant-dashboard')
        else:
            return render(request,'baseapp/consultant_wait_for_approval.html')
    elif is_client(request.user):
        accountapproval=models.Client.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('client-dashboard')
        else:
            return render(request,'baseapp/client_wait_for_approval.html')



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

def admin_dashboard_view(request):
    # for both table in admin dashboard
    consultants=models.Consultant.objects.all().order_by('-id')
    clients=models.Client.objects.all().order_by('-id')
    messages=models.Message.objects.all().order_by('-id')
    #for three cards
    consultantcount=models.Consultant.objects.all().filter(status=True).count()
    pendingconsultantcount=models.Consultant.objects.all().filter(status=False).count()

    clientcount=models.Client.objects.all().filter(status=True).count()
    pendingclientcount=models.Client.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()

    
    messagescount=models.Message.objects.all().filter(status=True).count()
    pendingmessagescount=models.Message.objects.all().filter(status=False).count()
    context = {
    'consultants':consultants,
    'clients':clients,
    'messages':messages,
    'consultantcount':consultantcount,
    'pendingconsultantcount':pendingconsultantcount,
    'clientcount':clientcount,
    'pendingclientcount':pendingclientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'messagescount':messagescount,
    'pendingmessagescount':pendingmessagescount,
    }
    return render(request,'baseapp/admin_dashboard.html', context)


# this view for sidebar click on admin page

def admin_consultant_view(request):
    return render(request,'baseapp/admin_consultant.html')




def admin_view_consultant_view(request):
    consultants = models.Consultant.objects.all().filter(status=True)
    context = {'consultants':consultants}
    return render(request,'baseapp/admin_view_consultant.html', context)




def delete_consultant_from_hospital_view(request,pk):
    consultant=models.Consultant.objects.get(id=pk)
    user=models.User.objects.get(id=consultant.user_id)
    user.delete()
    consultant.delete()
    return redirect('admin-view-consultant')




def update_consultant_view(request,pk):
    consultant=models.Consultant.objects.get(id=pk)
    user=models.User.objects.get(id=consultant.user_id)

    userForm=forms.ConsultantUserForm(instance=user)
    context = {'userForm':userForm}
    if request.method=='POST':
        userForm=forms.ConsultantUserForm(request.POST,instance=user)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            return redirect('admin-view-consultant')
    return render(request,'baseapp/admin_update_consultant.html',context)





def admin_add_consultant_view(request):
    userForm=forms.ConsultantUserForm()
    context = {'userForm':userForm}
    if request.method=='POST':
        userForm=forms.ConsultantUserForm(request.POST)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            my_consultant_group = Group.objects.get_or_create(name='CONSULTANT')
            my_consultant_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-view-consultant')
    return render(request,'baseapp/admin_add_consultant.html',context)



def admin_approve_consultant_view(request):
    #those whose approval are needed
    consultants = models.Consultant.objects.all().filter(status=False)
    context = {'consultants':consultants}
    return render(request,'baseapp/admin_approve_consultant.html', context)



def approve_consultant_view(request,pk):
    consultant = models.Consultant.objects.get(id=pk)
    consultant.status=True
    consultant.save()
    return redirect('admin-approve-consultant')



def reject_consultant_view(request,pk):
    consultant = models.Consultant.objects.get(id=pk)
    user=models.User.objects.get(id=consultant.user_id)
    user.delete()
    consultant.delete()
    return redirect('admin-approve-consultant')



def admin_view_consultant_specialisation_view(request):
    consultants = models.Consultant.objects.all().filter(status=True)
    context = {'consultants':consultants}
    return render(request,'baseapp/admin_view_consultant_specialisation.html', context)



def admin_client_view(request):
    return render(request,'baseapp/admin_client.html')




def admin_view_client_view(request):
    clients = models.Client.objects.all().filter(status=True)
    context = {'clients':clients}
    return render(request,'baseapp/admin_view_client.html', context)




def delete_client_from_hospital_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-view-client')



def update_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)

    userForm=forms.ClientUserForm(instance=user)

    context = {'userForm':userForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST,instance=user)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            return redirect('admin-view-client')
    return render(request,'baseapp/admin_update_client.html', context)





def admin_add_client_view(request):
    userForm=forms.ClientUserForm()
    context = {'userForm':userForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-view-client')
    return render(request,'baseapp/admin_add_client.html',context)


def admin_inbox(request):
    adminRecivedmessages = Message.objects.filter(reciever=request.user)
    context = {'messages' : adminRecivedmessages}
    return render(request, 'baseapp/admin_inbox.html', context)


def admin_notifications(request):
    consultants=models.Consultant.objects.all().order_by('-id')
    clients=models.Client.objects.all().order_by('-id')
    messages=models.Message.objects.all().order_by('-id')
    #for three cards
    adminNotifcations =Notification.objects.filter(user=request.user).order_by('-timestamp')
    context = {'notifications' : adminNotifcations,'consultants':consultants,'clients':clients,'messages':messages,}
    return render(request, 'baseapp/admin_notifications.html', context)





#------------------FOR APPROVING CLIENTS BY ADMIN----------------------

def admin_approve_client_view(request):
    #those whose approval are needed
    clients = models.Client.objects.all().filter(status=False)
    context = {'clients':clients}
    return render(request,'baseapp/admin_approve_client.html', context)



def approve_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    client.status=True
    client.save()
    return redirect('admin-approve-client')



def reject_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-approve-client')


def admin_consultation_requests_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    context = {'appointments':appointments}
    return render(request,'baseapp/admin_consultation_requests.html', context)


#-----------------APPOINTMENT START----------------------------------------------------------------#####

def admin_appointment_view(request):
    return render(request,'baseapp/admin_appointment.html')



def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    context = {'appointments':appointments}
    return render(request,'baseapp/admin_view_appointment.html', context)



def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    context = {'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.consultantID=request.POST.get('consultantID')
            appointment.clientID=request.POST.get('clientID')
            appointment.category=request.POST.get('category')
            appointment.description=request.POST.get('description')
            appointment.notes=request.POST.get('notes')
            appointment.consultantName=models.User.objects.get(id=request.POST.get('consultantID')).first_name
            appointment.clientName=models.User.objects.get(id=request.POST.get('clientID')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'baseapp/admin_add_appointment.html',context)



def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    context = {'appointments':appointments}
    return render(request,'baseapp/admin_approve_appointment.html', context)




def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect('admin-approve-appointment')




def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')



#-----------------APPOINTMENT START----------------------------------------------------------------#####

def admin_messages_view(request):
    return render(request,'baseapp/admin_messages.html')



def admin_view_messages_view(request):
    messages=models.Message.objects.all().filter(status=True)
    context = {'messages':messages}
    return render(request,'baseapp/admin_view_messages.html', context)


def admin_read_messages_view(request):
    #those whose approval are needed
    messages=models.Message.objects.all().filter(status=False)
    context = {'messages':messages}
    return render(request,'baseapp/admin_read_messages.html', context)


def read_messages_view(request,pk):
    message=models.Message.objects.get(id=pk)
    message.status=True
    message.save()
    return redirect('admin-read-messages')


def unread_messages_view(request,pk):
    message=models.Message.objects.get(id=pk)
    message.delete()
    return redirect('admin-read-messages')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ CONSULTANT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

def consultant_dashboard_view(request):
    # for three cards
    clientcount=models.Client.objects.all().filter(status=True,assignedConsultantID=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id).count()
    messagescount=models.Message.objects.all().filter(status=True,consultantID=request.user.id).count()
    # clientdischarged=models.ClientDischargeDetails.objects.all().distinct().filter(assignedConsultantName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id).order_by('-id')
    messages=models.Message.objects.all().filter(status=True,consultantID=request.user.id).order_by('-id')
    clientID=[]
    for appointment in appointments:
        clientID.append(appointment.clientID)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientID).order_by('-id')
    appointments=zip(appointments,clients, messages)
    context = {
    'clientcount':clientcount,
    'appointmentcount':appointmentcount,
    'messagescount':messagescount,
    # 'clientdischarged':clientdischarged,
    'appointments':appointments,
    'consultant':models.Consultant.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'baseapp/consultant_dashboard.html', context)



def consultant_client_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id)
    context =   {'consultant': consultant}
   #for profile picture of CONSULTANT in sidebar}
    return render(request,'baseapp/consultant_client.html',context)




def consultant_view_client_view(request):
    clients = models.Client.objects.all().filter(status=True,assignedConsultantID=request.user.id)
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    context = {'clients':clients,'consultant':consultant}
    return render(request,'baseapp/consultant_view_client.html', context)




def consultant_view_discharge_client_view(request):
    dischargedclients = models.ClientDischargeDetails.objects.all().distinct().filter(assignedConsultantName=request.user.first_name)
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of cosultant in sidebar
    context = {'dischargedclients':dischargedclients,'consultant':consultant}
    return render(request,'baseapp/consultant_view_discharge_client.html', context)



def consultant_appointment_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of COSULTANT in sidebar
    context = {'consultant':consultant}
    return render(request,'baseapp/consultant_appointment.html', context)



def consultant_view_appointment_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id)
    clientID=[]
    for appointment in appointments:
        clientID.append(appointment.clientID)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientID)
    appointments=zip(appointments, clients)
    context = {'appointments':appointments,'consultant':consultant, 'clients' : clients}
    return render(request,'baseapp/consultant_view_appointment.html', context)




def consultant_delete_appointment_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    clientID=[]
    for appointment in appointments:
        clientID.append(appointment.clientID)
    clients = models.Client.objects.all().filter(status=True,user_id__in=clientID)
    appointments=zip(appointments, clients)
    context = {'appointments':appointments,'consultant':consultant}
    return render(request,'baseapp/consultant_delete_appointment.html', context)



def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,consultantID=request.user.id)
    clientID=[]
    for appointment in appointments:
        clientID.append(appointment.clientID)
    clients = models.Client.objects.all().filter(status=True,user_id__in=clientID)
    appointments=zip(appointments, clients)
    context = {'appointments':appointments,'consultant':consultant}
    return render(request,'baseapp/consultant_delete_appointment.html', context)


def consultant_inbox(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id)
    consultantRecivedmessages = Message.objects.filter(reciever=request.user)
    context = {'messages' : consultantRecivedmessages, 'consultant' : consultant}
    return render(request, 'baseapp/consultant_inbox.html', context)



def consultant_notifications(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id)
    consultantNotifcations =Notification.objects.filter(user=request.user).order_by('-timestamp')
    context = {'notifications' : consultantNotifcations}
    return render(request, 'baseapp/consultant_notifications.html', context)




def consultantServicesView(request, username):
    services = ConsultancyService.objects.filter(consultant__username=username)
    context = {'services': services}
    return render(request, 'baseapp/consultantServices.html', context)



def consultancyServiceDetail(request, serviceID):
    service = get_object_or_404(ConsultancyService, id=serviceID)
    if request.method == 'POST':
        ConsultationRequest.objects.create(
            client=request.user,
            consultant=service.consultant,
            service=service
        )
        return redirect('profile', username=request.user.username)
    context = {'service' : service}
    return render(request, 'baseapp/serviceDetail.html', context)



def manageAppointments(request):
    appointments = Appointment.objects.filter(client=request.user.client)
    context = {'appiontments' : appointments}
    return render(request, 'baseapp/manage_appiontments.html', context)


def acceptDeclineRequest(request, requestID, action):
    consultationRequest = get_object_or_404(ConsultationRequest, id=requestID)
    if action == 'accept':
        consultationRequest.requestStatus = 'accepted'
        consultationRequest.save()
    elif action == 'decline':
        consultationRequest.requestStatus = 'declined'
        consultationRequest.save()
    return redirect('consultation_request')


def respond_appointment_request(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    client = appointment.client
    
    if request.method == 'POST':
        form = AppointmentResponseForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            
            # Update the appointment status
            appointment.status = response
            appointment.save()
            
            # Create a notification for the client
            message = f"Your appointment request has been {response}."
            notification = Notification(user=client, message=message)
            notification.save()
            
            return redirect('appointment_response_confirmation')  # Redirect to a confirmation page
    else:
        form = AppointmentResponseForm()
    
    return render(request, 'consultancy/respond_appointment_request.html', {'form': form, 'appointment': appointment})




def respond_to_client(request, client_id):
    client = User.objects.get(id=client_id)
    
    if request.method == 'POST':
        response_message = request.POST['response_message']  # Adjust this based on your form
        # Your response logic here...

        # Create a notification for the client
        message = f"A response has been received from the consultant: {response_message}"
        notification = Notification(user=client, message=message)
        notification.save()

        return redirect('response_confirmation')  # Redirect to a confirmation page

    return render(request, 'consultancy/respond_to_client.html', {'client': client})



def consultant_view_messages_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of CONSULTANT in sidebar
    messages=models.Message.objects.all().filter(status=True,consultantID=request.user.id)
    clientID=[]
    for m in messages:
        clientID.append(m.clientID)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientID)
    messages=zip(messages, clients)
    context = {'messages':messages,'consultant':consultant, 'clients' : clients}
    return render(request,'baseapp/consultant_view_messages.html', context)



def consultant_messages_view(request):
    consultant = models.Consultant.objects.get(user_id=request.user.id) #for profile picture of COSULTANT in sidebar
    context = {'consultant':consultant}
    return render(request,'baseapp/consultant_messages.html', context)



#---------------------------------------------------------------------------------
#------------------------ CONSULTANT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------




#---------------------------------------------------------------------------------
#------------------------ CLIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

def client_dashboard_view(request):
    client = models.Client.objects.get(user_id=request.user.id)
    appointments=models.Appointment.objects.all().filter(clientID=request.user.id)
    consultant = models.Consultant.objects.get(user_id=client.assignedConsultantID)
    context = {'client': client,'consultantName': consultant.get_name, 'consultantEmail' : consultant.email, 'serviceRequestDate' : client.siteRegisterDate, 'appointments':appointments}
    return render(request,'baseapp/client_dashboard.html',context)



def client_appointment_view(request):
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    context = {'client':client}
    return render(request,'baseapp/client_appointment.html', context)



def client_book_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    context = {'appointmentForm':appointmentForm,'client': client}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.consultantID=request.POST.get('consultantID')
            appointment.clientID=request.user.id #----user can choose any client but only their info will be stored
            appointment.category=request.POST.get('category')
            appointment.description=request.POST.get('description')
            appointment.notes=request.POST.get('notes')
            appointment.consultantName=models.User.objects.get(id=request.POST.get('consultantID')).first_name
            appointment.clientName=request.user.first_name #----user can choose any CLIENT but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('client-view-appointment')
    return render(request,'baseapp/client_book_appointment.html',context)






def client_view_appointment_view(request):
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    appointments=models.Appointment.objects.all().filter(clientID=request.user.id)
    context = {'appointments':appointments,'client':client}
    return render(request,'baseapp/client_view_appointment.html', context)



def consultant_detail(request, consultant_id):
    consultant = get_object_or_404(Consultant, id=consultant_id)
    context = {'consultant' : consultant}
    return render(request, 'baseapp/consultant_detail.html', context)



def client_inbox(request):
    client = models.Client.objects.get(user_id=request.user.id)
    clientRecivedmessages = Message.objects.filter(reciever=request.user)
    context = {'messages' : clientRecivedmessages}
    return render(request, 'baseapp/client_inbox.html', context)


def client_notifications(request):
    client = models.Client.objects.get(user_id=request.user.id)
    appointments=models.Appointment.objects.all().filter(clientID=request.user.id)
    messages=models.Message.objects.all().filter(clientID=request.user.id)
    consultant = models.Consultant.objects.get(user_id=client.assignedConsultantID)
    context = {'messages':messages, 'client': client,'consultantName': consultant.get_name, 'consultantEmail' : consultant.email, 'serviceRequestDate' : client.siteRegisterDate, 'appointments':appointments}
    return render(request, 'baseapp/client_notifications.html', context)




def scheduleAppointment(request, consultant_id):
    consultant = get_object_or_404(Consultant, id=consultant_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.consultant = consultant
            appointment.save()
            return redirect('appointment_confirmation')
    else:
        form = AppointmentForm()
    context = {'form' : form, 'consultant' : consultant}
    return render(request, 'baseapp/schedule_appointment.html', context)


def cancelAppointment(request, appointment_id):
    appiontment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.client == appiontment.client:
        appiontment.delete()

    return redirect('manage_appointments')



def sendMessage(request, reciever_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        reciever = User.objects.get(id=reciever_id)
        message = Message.objects.create(sender=request.user, reciever=reciever, content=content)
        message.save()

        notification = Notification.objects.create(user=reciever, message=f'You have a New Message from {request.user}')
        notification.save()

        return redirect('inbox')



def client_send_messages_view(request):
    messageForm=forms.MessageForm()
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    context = {'messageForm':messageForm,'client': client}
    if request.method=='POST':
        messageForm=forms.MessageForm(request.POST)
        if messageForm.is_valid():
            message=messageForm.save(commit=False)
            message.consultantID=request.POST.get('consultantID')
            message.clientID=request.user.id #----user can choose any client but only their info will be stored
            message.content=request.POST.get('content')
            message.consultantName=models.User.objects.get(id=request.POST.get('consultantID')).first_name
            message.clientName=request.user.first_name #----user can choose any CLIENT but only their info will be stored
            message.status=False
            message.save()
        return HttpResponseRedirect('client-view-messages')
    return render(request,'baseapp/client_send_messages.html',context)


def client_view_messages_view(request):
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    messages=models.Message.objects.all().filter(clientID=request.user.id)
    context = {'messages':messages,'client':client}
    return render(request,'baseapp/client_view_messages.html', context)



def client_messages_view(request):
    client = models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    context = {'client':client}
    return render(request,'baseapp/client_messages.html', context)



#------------------------ CLIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'baseapp/aboutus.html')

def contactus_view(request):
    subscribeForm = forms.ContactusForm()
    if request.method == 'POST':
        subscribeForm = forms.ContactusForm(request.POST)
        if subscribeForm.is_valid():
            email = subscribeForm.cleaned_data['Email']
            name=subscribeForm.cleaned_data['Name']
            message = subscribeForm.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'baseapp/contactussuccess.html')
        context = {'form':subscribeForm}
    return render(request, 'baseapp/contactus.html', context)













#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#####







def consultationRequest(request):
    consultationRequests = ConsultationRequest.objects.filter(consultant=request.user)
    context = {'consultationRequests' : consultationRequests}
    return render(request, 'baseapp/consultationRequests.html', context)




















def request_appointment(request, consultant_id):
    consultant = User.objects.get(id=consultant_id)
    
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            # Your appointment request logic here...
            
            # Create a notification for the consultant
            message = f"A client has requested an appointment with you."
            notification = Notification(user=consultant, message=message)
            notification.save()
            
            return redirect('appointment_request_confirmation')  # Redirect to a confirmation page
    else:
        form = AppointmentRequestForm()
    
    return render(request, 'consultancy/request_appointment.html', {'form': form, 'consultant': consultant})










def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            
            # Create a notification for the recipient
            notification = Notification(user=recipient, message=message)
            notification.save()
            
            return redirect('message_sent_confirmation')  # Redirect to a confirmation page
    else:
        form = MessageForm()
    
    return render(request, 'consultancy/send_message.html', {'form': form, 'recipient': recipient})


def appointmentConfirmation(request):
    return render(request, 'baseapp/appointment_confirmation.html')








    









