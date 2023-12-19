from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages



def user_not_Admin(view_func):

    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='ADMIN').exists():
            messages.error(request, "You don't have Permission to access this page")
            return redirect('dating_app:adminPage')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
