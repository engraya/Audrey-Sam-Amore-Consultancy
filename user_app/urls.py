from django.urls import path
from . import views
from .views import CancelView, SuccessView

app_name = 'user_app'

urlpatterns = [

	path('main/', views.corePage, name='main'),
	path('client-ready/', views.clientReadyPage, name='client-ready'),
    path('client_signup/', views.client_signup, name='client_signup'),
    path('admin_signup/', views.admin_signup, name='admin_signup'),
    
	path('admin_sign_in', views.admin_login, name='admin_sign_in'),
	path('client_sign_in', views.client_login, name='client_sign_in'),
    path('adminclick', views.adminclick_view, name='adminclick'),
    path('clientclick', views.clientclick_view, name='clientclick'),
    
	path('afterlogin', views.afterlogin_view,name='afterlogin'),

	path('logout/', views.logout_user, name='logout_user'),

	path('signup/step_one/', views.sign_up_step_one, name='sign_up_step_one'),
	path('signup/step_two/', views.sign_up_step_two, name='sign_up_step_two'),
	path('signup/step_three/', views.sign_up_step_three, name='sign_up_step_three'),

	path('my_profile/', views.my_profile, name='my_profile'),
    path('contact-us', views.contactUs, name="contact"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),

    


]