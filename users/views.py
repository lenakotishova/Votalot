from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from mysite import settings

from django.views import generic
from django.urls import reverse_lazy


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('polls:index')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


def login_view(request):
    value_next = request.POST.get('next')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # if value_next in request.POST:
            #     return redirect(value_next)
            # else:
            #     return redirect('polls:details', pk=1)
        return redirect(value_next)
    else:
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form, 'value_next': value_next})

