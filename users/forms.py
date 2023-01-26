from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.forms import ModelForm, Textarea, CharField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            'class': 'form-class',
        }
        ),
    )
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-class'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-class'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-class'}))




    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ['username', 'email']
        # field_classes = {"username": UsernameField}
        fields = UserCreationForm.Meta.fields + ('username', 'email',)






