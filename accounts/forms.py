from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import ProfileUser


class UserCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=17, min_length=4, required=True, help_text='Як Вас звати?', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ваше ім'я"}))
    
    last_name = forms.CharField(max_length=17, min_length=4, required=True, help_text='Ваша фамілія', widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ваша фамілія"})))
    
    email = forms.EmailField(max_length=50, help_text='Веддіть свою пошту (потрібно для випадків втрати доступу до власного кабінету).', widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})))
    
    password1 = forms.CharField(label=_('Пароль:'), widget=(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})), help_text=password_validation.password_validators_help_text_html())
    
    password2 = forms.CharField(label=_('Підтвердіть пароль'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль ще раз'}),
                                help_text=_('Введіть пароль ще раз'))
    
    username = forms.CharField(
        label=_("Номер телефону для входу в особистий кабінет"),
        max_length=13,
        min_length=10,
        help_text=_('Формат: 0671234567'),
        
        error_messages={'unique': _("Користувач з таким номером телефону вже зареєстрованний")},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0671234567', 'pattern':'[0]{1}[4-9]{1}[2-9]{1}[0-9]{7}'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class ProfileUserForm(ModelForm):

    class Meta:
        model = ProfileUser
        fields = ('city', 'delivery', 'birthday', )