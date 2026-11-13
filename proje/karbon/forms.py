from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Kullanıcı Adı"
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Şifre"
        self.fields['password2'].label = "Şifreyi Tekrarlayın"
    class Meta:
        model=User
        fields=('username','email','password1','password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(),label="Kullanıcı Adı")
    password = forms.CharField(widget=PasswordInput(),label="Şifre")

class EmissionForm(forms.Form):

    electricity = forms.FloatField(
        label="Elektrik (kWh)",
        min_value=0
    )

    natural_gas = forms.FloatField(
        label="Doğalgaz (m³)",
        min_value=0
    )

    FUEL_CHOICES = [
        ('benzin', 'Benzin'),
        ('dizel', 'Dizel'),
        ('lpg', 'LPG'),
    ]

    fuel_type = forms.ChoiceField(
        choices=FUEL_CHOICES,
        label="Yakıt Türü"
    )

    fuel_amount = forms.FloatField(
        label="Yakıt Miktarı (litre)",
        min_value=0
    )

class PasswordChangingForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].label = "Eski Şifre"
        self.fields['new_password1'].label = "Yeni Şifre"
        self.fields['new_password2'].label = "Yeni Şifre Tekrar"