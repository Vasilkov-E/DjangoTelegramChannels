from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .form import NameForm, CreateUserForm, File
from .functions import *


@login_required(login_url='login')
@csrf_protect
def table(request):
    try:
        if request.method == 'GET':
            all_channels = Channels.objects.filter(name__contains=request.GET['q'])
            return render(request, 'TelegramChannels/table.html', context=get_our_home_page(request, all_channels))
    except:
        pass
    if request.method == 'POST':
        print(request.POST)

        for i in request.POST.items():
            if i[0] == 'del':
                delete_from_db(request.POST)
                break
            elif i[0] != 'edit' and i[0] != 'csrfmiddlewaretoken':
                return HttpResponseRedirect(f"/TelegramChannels/edit/{i[0]}")

        all_channels = Channels.objects.all()
    else:
        all_channels = Channels.objects.all()
    return render(request, 'TelegramChannels/table.html', context=get_our_home_page(request, all_channels))


def log_out(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def add_channel(request):
    if request.method == 'POST':
        form = NameForm(request.POST, request.FILES)
        if form.is_valid():
            add(form.cleaned_data)
    else:
        form = NameForm()
    return render(request, 'TelegramChannels/AddChannel.html', {'form': form})


def channel(request, number):
    channel = Channels.objects.get(id__iexact=number)
    return render(request, 'TelegramChannels/Chennel.html', context={'channel': channel})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'TelegramChannels/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'TelegramChannels/login.html', context)


def home(request):
    try:
        if request.method == 'GET':
            all_channels = Channels.objects.filter(name__contains=request.GET['q'])
            return render(request, 'TelegramChannels/ChennelHome.html',
                          context=get_our_home_page(request, all_channels))
    except:
        pass
    if request.method == 'POST':
        delete_from_db(request.POST)
        all_channels = Channels.objects.all()
    else:
        all_channels = Channels.objects.all()
    return render(request, 'TelegramChannels/ChennelHome.html', context=get_our_home_page(request, all_channels))


@login_required(login_url='login')
def edit(request, id=0):
    try:
        print(request.POST)
        person = Channels.objects.get(id=id)
        old_adres = person.adres_img_for_general_information_about_the_resource
        if request.method == "POST":
            f = File(request.POST, request.FILES)
            if f.is_valid():
                # print(f.cleaned_data['adres'])
                person.name = request.POST.get('name')
                person.general_information_about_the_resource = request.POST.get(
                    'general_information_about_the_resource')
                person.adres_img_for_general_information_about_the_resource = f.cleaned_data['adres']
                person.name_administrator = request.POST.get('name_administrator')
                person.other = request.POST.get('other')
                person.date_of_resourc_creation = request.POST.get('date_of_resourc_creation')
                person.resource_content_date = request.POST.get('resource_content_date')
                person.publications_per_day = request.POST.get('publications_per_day')
                person.the_main_focus_of_the_channel = request.POST.get('the_main_focus_of_the_channel')
                person.related_areas = request.POST.get('related_areas')
                person.channel_content = request.POST.get('channel_content')
                person.views = request.POST.get('views')
                person.save()
                delete_file(old_adres)
            return HttpResponseRedirect("/TelegramChannels/table")
        else:
            return render(request, "TelegramChannels/edit.html", {"form": person, "file": File()})
    except Channels.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
