from django.urls import path

from . import views

urlpatterns = [
    path('table/', views.table, name='table'),
    path('add/', views.add_channel, name='add_channel'),
    path('channel/<int:number>/', views.channel, name='channel'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('', views.home, name='home'),
    path('edit/<int:id>/', views.edit, name="edit"),

]
