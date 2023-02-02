from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
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
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-class'}), label='Username')
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-class'}), label='What should we call you?')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-class'}), label='Your password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-class'}),
        label='Confirm your password')

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ['username', 'email']
        # field_classes = {"username": UsernameField}
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'email',)


class AuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": 'form-class'}))
    password = forms.CharField(label=_("Password"), strip=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
