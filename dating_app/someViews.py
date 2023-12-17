@login_required
def userList(request):
	users = User.objects.filter(profile__isnull=False)
	context = {'users' : users}
	return render(request, 'users.html', context)

@login_required
def profileDetail(request, user_id):
	userProfile = get_object_or_404(Profile, user_id=user_id)
	context = {'profile' : userProfile}
	return render(request, 'partner_account.html', context)





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
def dating(request):
	users = User.objects.filter(profile__isnull=False)
	context = {'users' : users}
	return render(request, 'dating.html', context)


@login_required
def partner_account(request, user_id):
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