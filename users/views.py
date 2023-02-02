from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreationForm, AuthenticationForm
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


class Login(View):
    def get(self, request):
        context = {
            'form': AuthenticationForm()
        }
        return render(request, self.template_name, context)

    def user_login(self, request):
        form = AuthenticationForm(request.POST or None)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})
