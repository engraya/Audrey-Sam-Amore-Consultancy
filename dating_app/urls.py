from django.urls import path, include
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'dating_app'

urlpatterns = [
    path('', views.dating, name='dating'),
    path('admin', views.adminPage, name='adminPage'),
    path('favorite/add/<int:user_id>/', views.favorite_add, name='favorite_add'),
    path('random_card/', views.random_card, name='random_card'),
    path('<int:user_id>/', views.partner_account, name='partner_account'),

    path('admin-dashboard', views.admin_dashboard_view, name="admin-dashboard"),
    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment,name='reject-appointment'),

    path('admin-messages', views.admin_messages_view,name='admin-messages'),
    path('admin-view-messages', views.admin_view_messages_view,name='admin-view-messages'),
    path('admin-send-messages', views.admin_send_messages_view,name='admin-send-messages'),
    path('admin-read-messages', views.admin_read_messages_view,name='admin-read-messages'),
    path('approve-messages/<int:pk>', views.read_messages,name='read-messages'),
    path('reject-messages/<int:pk>', views.reject_messages,name='reject-messages'),


    
    path('admin-client/', views.admin_client_view,name='admin-client'),
    path('admin-view-client/', views.admin_view_client_view,name='admin-view-client'),
    path('delete-client/<int:pk>', views.delete_client_view,name='delete-client'),

    path('client-dashboard', views.client_dashboard_view, name="client-dashboard"),
    path('client-appointment', views.client_appointment_view,name='client-appointment'),
    path('client-book-appointment', views.client_book_appointment,name='client-book-appointment'),
    path('client-view-appointment', views.client_view_appointment_view,name='client-view-appointment'),


    path('client-messages', views.client_messages_view,name='client-messages'),
    path('client-send-messages', views.client_send_messages,name='client-send-messages'),
    path('client-view-messages', views.client_view_messages_view,name='client-view-messages'),
    path('client-read-messages', views.client_read_messages_view,name='client-read-messages'),
    path('cancel-appointment', views.client_cancel_appointment_view, name="cancel-appointment"),


    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('schedule_appointment/<int:admin_id>/', views.schedule_appointment, name='schedule_appointment'),
    path('message_list/', views.message_list, name='message_list'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),



]