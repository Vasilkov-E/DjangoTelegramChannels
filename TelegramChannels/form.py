from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class NameForm(forms.Form):
    name = forms.CharField(label='Name')
    general_information_about_the_resource = forms.CharField(label='Your name')
    # forms.CharField(widget=forms.Textarea)
    # Причетні до ресурсу особи

    name_administrator = forms.CharField(label='ФІО')
    other = forms.CharField(widget=forms.Textarea)
    # Вміст ресурсу
    adres_img_for_general_information_about_the_resource = forms.FileField()
    date_of_resourc_creation = forms.CharField(label='Дата створення ресурсу')
    resource_content_date = forms.CharField(label='Вміст ресурсу станом на:')
    publications_per_day = forms.CharField(label='публікацій в день')
    the_main_focus_of_the_channel = forms.CharField(label='Основна спрямованість каналу')
    related_areas = forms.CharField(label='Суміжні напрямки')
    channel_content = forms.CharField(label='Вміст каналу')
    views = forms.CharField(label='Перегляди')

class File(forms.Form):
    adres = forms.FileField()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        captcha = ReCaptchaField()
        fields = ['username', 'email', 'password1', 'password2']
