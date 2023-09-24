from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import User
from .models import Message
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dating_app.models import Favorite


class MessagesListView(LoginRequiredMixin, ListView):

	model = Message
	template_name = 'chat_app/messages_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk) 
		messages = Message.get_message_list(user) 

		other_users = [] 

	
		for i in range(len(messages)):
			if messages[i].sender != user:
				other_users.append(messages[i].sender)
			else:
				other_users.append(messages[i].recipient)


		context['messages_list'] = messages
		context['other_users'] = other_users
		context['user'] = user
		context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')
		return context


class InboxView(LoginRequiredMixin, DetailView):
	
	model = Message
	template_name = 'chat_app/inbox.html'
	queryset = User.objects.all()


	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(self.request, *args, **kwargs)

	
	def get_object(self):
		UserName= self.kwargs.get("username")
		return get_object_or_404(User, username=UserName)



	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk)  
		other_user = User.objects.get(username=self.kwargs.get("username")) 
		messages = Message.get_message_list(user) 

		other_users = []

	
		for i in range(len(messages)):
			if messages[i].sender != user:
				other_users.append(messages[i].sender)
			else:
				other_users.append(messages[i].recipient)

		sender = other_user  
		recipient = user 

		context['messages'] = Message.get_all_messages(sender, recipient) 
		context['messages_list'] = messages 
		context['other_person'] = other_user  
		context['user'] = user 
		context['other_users'] = other_users
		context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')

		return context


	def post(self, request, *args, **kwargs):
		sender = User.objects.get(pk=request.POST.get('user')) 
		recipient = User.objects.get(pk=request.POST.get('recipient')) 
		message = request.POST.get('message')  

		if request.user.is_authenticated:
			if request.method == 'POST':
				if message:
					Message.objects.create(sender=sender, recipient=recipient, message=message)
			return redirect('chat_app:inbox', username=recipient.username)  

		else:
			# return render(request, 'auth/login.html')
			pass

class UserListsView(LoginRequiredMixin, ListView):
	"""Список пользователей"""
	model = User
	template_name = 'chat_app/users_list.html'
	context_object_name = 'users'

	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk)  
		context['users'] = User.objects.exclude(pk=user.pk)  
		return context



class ChatView(LoginRequiredMixin, DetailView):

	model = Message
	template_name = 'chat_app/chat.html'
	queryset = User.objects.all()


	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(self.request, *args, **kwargs)


	def get_object(self):
		UserName= self.kwargs.get("username")
		return get_object_or_404(User, username=UserName)




	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk) 
		other_user = User.objects.get(username=self.kwargs.get("username"))  
		messages = Message.get_message_list(user) 

		other_users = [] 

		
		for i in range(len(messages)):
			if messages[i].sender != user:
				other_users.append(messages[i].sender)
			else:
				other_users.append(messages[i].recipient)

		sender = other_user
		recipient = user 

		context['messages'] = Message.get_all_messages(sender, recipient)  
		context['messages_list'] = messages 
		context['other_person'] = other_user  
		context['user'] = user 
		context['other_users'] = other_users
		context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')

		return context

  
	def post(self, request, *args, **kwargs):

		sender = User.objects.get(pk=request.POST.get('user'))  
		recipient = User.objects.get(pk=request.POST.get('recipient')) 
		message = request.POST.get('message')  

	
		if request.user.is_authenticated:
			if request.method == 'POST':
				if message:
					Message.objects.create(sender=sender, recipient=recipient, message=message)
			return redirect('chat_app:message_list', username=recipient.username)  

		else:
			# return render(request, 'auth/login.html')
			pass