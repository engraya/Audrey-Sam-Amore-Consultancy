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
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),

    
    path('admin-client/', views.admin_client_view,name='admin-client'),
    path('admin-view-client/', views.admin_view_client_view,name='admin-view-client'),
    path('delete-client/<int:pk>', views.delete_client_view,name='delete-client'),

    path('client-dashboard', views.client_dashboard_view, name="client-dashboard"),
    path('client-appointment', views.client_appointment_view,name='client-appointment'),
    path('client-view-appointment', views.client_view_appointment_view,name='client-view-appointment'),


    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('schedule_appointment/<int:admin_id>/', views.schedule_appointment, name='schedule_appointment'),
    path('message_list/', views.message_list, name='message_list'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),



]