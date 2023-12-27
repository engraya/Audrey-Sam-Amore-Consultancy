from django.urls import path
from . import views

app_name = 'dating_app'

urlpatterns = [

    path('profileDetail/<int:user_id>/', views.profileDetail, name="profileDetail"),

    path('', views.dating, name='dating'),
    path('admin', views.adminPage, name='adminPage'),

    path('admin-dashboard', views.admin_dashboard_view, name="admin-dashboard"),
    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment,name='reject-appointment'),
    path('appointment/<int:pk>', views.appointmentDetail, name='appointment-detail'),
    path('admin-appointment-history', views.admin_appointment_history_view, name='admin-appointment-history'),

    path('admin-messages', views.admin_messages_view,name='admin-messages'),
    path('admin-view-messages', views.admin_view_messages_view,name='admin-view-messages'),
    path('admin-send-messages', views.admin_send_messages_view,name='admin-send-messages'),
    path('admin-read-messages', views.admin_read_messages_view,name='admin-read-messages'),
    path('admin-outbox', views.admin_outbox, name='admin-outbox'),
    path('approve-messages/<int:pk>', views.read_messages,name='read-messages'),
    path('reject-messages/<int:pk>', views.reject_messages,name='reject-messages'),
    path('admin-reply-messages', views.admin_reply_messages_view, name='admin-reply-messages'),
    path('message/<int:pk>', views.adminMessageDetail, name='message-detail'),

    
    path('admin-client/', views.admin_client_view,name='admin-client'),
    path('admin-view-client/', views.admin_view_client_view,name='admin-view-client'),
    path('delete-client/<int:pk>', views.delete_client_view,name='delete-client'),

    path('client-dashboard', views.client_dashboard_view, name="client-dashboard"),
    path('client-dashboard', views.clientPage, name='clientPage'),
    path('client-appointment', views.client_appointment_view,name='client-appointment'),
     path('clientAppointment/<int:pk>', views.client_Appointment_Detail, name='appointmentdetail'),
    path('client-book-appointment', views.client_book_appointment,name='client-book-appointment'),
    path('client-view-appointment', views.client_view_appointment_view,name='client-view-appointment'),
    path('client-appointment-history', views.client_appointment_history, name='client-appointment-history'),
    path('cancel-appointment/<int:pk>', views.client_cancel_appointment_view, name="cancel-appointment"),


    path('client-messages', views.client_messages_view,name='client-messages'),
    path('message/<int:pk>', views.messageDetail, name='message-detail'),
    path('client-send-messages', views.client_send_messages,name='client-send-messages'),
    path('client-view-messages', views.client_view_messages_view,name='client-view-messages'),
    path('client-read-messages', views.client_read_messages_view,name='client-read-messages'),
    path('client-outbox', views.client_messages_outbox, name="client-outbox"),
    path('read-messages/<int:pk>', views.client_read_messages, name='read-messages'),
    path('delete-message/<int:pk>', views.client_delete_messages, name="delete-message"),



]