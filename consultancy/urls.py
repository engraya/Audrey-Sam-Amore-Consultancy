from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.i18n import i18n_patterns

app_name = 'consultancy'


urlpatterns = [

    path('',views.home_view,name='home'),

    

        #password Reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="baseapp/passwordManage/passwordManage/password_reset_form.html"), name="reset_password"),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name="baseapp/passwordManage/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="baseapp/passwordManage/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="baseapp/passwordManage/password_reset_complete.html"), name="password_reset_complete"),

 

   
    path('service/<int:serviceID>', views.consultancyServiceDetail, name="service_detail"),
    path('consultation/requests', views.consultationRequest, name="consultation_request"),
    path('consultation/requests/<int:requestID>/<str:action>/', views.acceptDeclineRequest, name="accept_decline_request"),



    path('send_message/<int:reciever_id>/', views.sendMessage, name="send_messsage"),


    path('consultants', views.consultantsList, name="consultants"),
    path('consultant/<str:consultant_id>', views.consultant_detail, name="consultant_detail"),


    path('scheduleAppointment/<int:consultant_id>/', views.scheduleAppointment, name="schedule_appointment"),
    path("appointment_confirmation", views.appointmentConfirmation, name="appointment_confirmation"),
    path('appointments/', views.manageAppointments, name="manage_appointments"),
    path('appointment/<int:appoinntment_id>/cancel', views.cancelAppointment, name="cancel_appointment"),
    path('request_appointment/<int:consultant_id>/', views.request_appointment, name='request_appointment'),
    path('respond_appointment_request/<int:appointment_id>/', views.respond_appointment_request, name='respond_appointment_request'),
    path('respond_to_client/<int:client_id>/', views.respond_to_client, name='respond_to_client'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),




    # path('book_appointment/', views.AppointmentTemplateView.as_view(), name='book'),
    # path('manage-appointments/', views.ManageAppointmentTemplateView.as_view(), name='manage'),




    # path('notifications', views.notiifcations, name='notifications'),
    # path('messaging/<str:recipientUsername>/', views.messaging, name='messaging'),
    # path('send_message/', views.sendMessage, name='sendMessage'),
    # path('get_notifications_message_count/', views.notificationsMessageCount, name='get_notifications_message_count'),
    # path('loadMessages/<str:recipient_username>/', views.loadMessages, name='loadMessages'),

    
    path('adminclick', views.adminclick_view, name="adminclick"),
    path('consultantclick', views.consultantclick_view, name="consultantclick"),
    path('clientclick', views.clientclick_view, name="clientclick"),


    path('adminsignup', views.admin_signup_view),
    path('consultantsignup', views.consultant_signup_view,name='consultantsignup'),
    path('clientsignup', views.client_signup_view),
    path('adminlogin', LoginView.as_view(template_name='baseapp/adminlogin.html')),
    path('consultantlogin', LoginView.as_view(template_name='baseapp/consultantlogin.html')),
    path('clientlogin', LoginView.as_view(template_name='baseapp/clientlogin.html')),



    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='baseapp/homePage.html'),name='logout'),


    #---------FOR DASHBOARD RELATED URLS-------------------------------------####
    
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('consultant-dashboard', views.consultant_dashboard_view,name='consultant-dashboard'),
    path('client-dashboard', views.client_dashboard_view,name='client-dashboard'),


    path('admin-consultant', views.admin_consultant_view,name='admin-consultant'),
    path('admin-view-consultant', views.admin_view_consultant_view,name='admin-view-consultant'),
    path('delete-consultant-from-hospital/<int:pk>', views.delete_consultant_from_hospital_view,name='delete-consultant-from-hospital'),
    path('update-consultant/<int:pk>', views.update_consultant_view,name='update-consultant'),
    path('admin-add-consultant', views.admin_add_consultant_view,name='admin-add-consultant'),
    path('admin-approve-consultant', views.admin_approve_consultant_view,name='admin-approve-consultant'),
    path('approve-consultant/<int:pk>', views.approve_consultant_view,name='approve-consultant'),
    path('reject-consultant/<int:pk>', views.reject_consultant_view,name='reject-consultant'),
    path('admin-view-consultant-specialisation',views.admin_view_consultant_specialisation_view,name='admin-view-consultant-specialisation'),



    path('admin-client', views.admin_client_view,name='admin-client'),
    path('admin-view-client', views.admin_view_client_view,name='admin-view-client'),
    path('delete-client-from-hospital/<int:pk>', views.delete_client_from_hospital_view,name='delete-client-from-hospital'),
    path('update-client/<int:pk>', views.update_client_view,name='update-client'),
    path('admin-add-client', views.admin_add_client_view,name='admin-add-client'),
    path('admin-approve-client', views.admin_approve_client_view,name='admin-approve-client'),
    path('approve-client/<int:pk>', views.approve_client_view,name='approve-client'),
    path('reject-client/<int:pk>', views.reject_client_view,name='reject-client'),
    # path('admin-discharge-client', views.admin_discharge_client_view,name='admin-discharge-client'),
    # path('admin-press-client', views.admin_press_client_view,name='admin-press-client'),
    # path('discharge-client/<int:pk>', views.discharge_client_view,name='discharge-client'),
    # path('press-client/<int:pk>', views.press_client_view,name='press-client'),
    # path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
    path('admin-inbox', views.admin_inbox,name='admin-inbox'),
    path('admin-notifications', views.admin_notifications,name='admin-notifications'),

    path('admin-messages', views.admin_messages_view,name='admin-messages'),
    path('admin-view-messages', views.admin_view_messages_view,name='admin-view-messages'),
    path('admin-read-messages', views.admin_read_messages_view,name='admin-read-messages'),
    path('read-messages/<int:pk>', views.read_messages_view,name='read-message'),
    path('unread-messsages/<int:pk>', views.unread_messages_view,name='unread-message'),
    path('admin-consultation-requests', views.admin_consultation_requests_view,name='admin-consultation-requests'),

   

]


#---------FOR CONSULTANT RELATED URLS-------------------------------------
urlpatterns +=[
    path('consultant-dashboard', views.consultant_dashboard_view,name='consultant-dashboard'),
    path('consultant-client', views.consultant_client_view,name='consultant-patient'),
    path('consultant-view-client', views.consultant_view_client_view,name='consultant-view-client'),
    path('consultant-view-discharge-patient',views.consultant_view_discharge_client_view,name='consultant-view-discharge-client'),
    path('consultant-appointment', views.consultant_appointment_view,name='consultant-appointment'),
    path('consultant-view-appointment', views.consultant_view_appointment_view,name='consultant-view-appointment'),
    path('consultant-delete-appointment',views.consultant_delete_appointment_view,name='consultant-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
    path('consultant-inbox', views.consultant_inbox,name='consultant-inbox'),
    path('consultant-notifications', views.consultant_notifications,name='consultant-notifications'),
    path("consultant/<str:username>/services", views.consultantServicesView, name="consultant_sevices"),

    path('consultant-messages', views.consultant_messages_view,name='consultant-messages'),
    path('consultant-view-messages', views.consultant_view_messages_view,name='consultant-view-messages'),
]



#---------FOR CLIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('client-dashboard', views.client_dashboard_view,name='client-dashboard'),
    path('client-appointment', views.client_appointment_view,name='client-appointment'),
    path('client-messages', views.client_messages_view,name='client-messages'),
    path('client-book-appointment', views.client_book_appointment_view,name='client-book-appointment'),
    path('client-send-messages', views.client_send_messages_view,name='client-send-messsages'),
    path('client-view-appointment', views.client_view_appointment_view,name='client-view-appointment'),
    path('client-view-messages', views.client_view_messages_view,name='client-view-messages'),
    # path('client-discharge', views.client_discharge_view,name='client-discharge'),
    path('client-inbox', views.client_inbox,name='client-inbox'),
    path('client-notifications', views.client_notifications,name='client-notifications'),


]
