from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# manage.py makemigrations     # для создания бд
# manage.py migrate


class Channels(models.Model):
    __tablename__ = 'channels'

    # Загальна інформація про ресурс

    id = models.AutoField(primary_key=True)
    name = models.TextField()  # название канала
    general_information_about_the_resource = models.TextField()  # Загальна інформація про ресурс
    adres_img_for_general_information_about_the_resource = models.ImageField(
        upload_to='%Y/%m/%d/')  # адрес картинки
    date_of_resourc_creation = models.TextField()  # Дата створення ресурсу

    # Причетні до ресурсу особи
    views = models.TextField()
    name_administrator = models.TextField()  # ФІО Адміністратора
    other = models.TextField()  #

    # Вміст ресурсу

    resource_content_date = models.TextField()  # Вміст ресурсу станом на:
    publications_per_day = models.TextField()  # публікацій в день
    the_main_focus_of_the_channel = models.TextField()  # Основна спрямованість каналу
    related_areas = models.TextField()  # Суміжні напрямки
    channel_content = models.TextField()  # Вміст каналу
    # adres_img_for_views = models.TextField()  # Ардес картинки для кол переглядів

    def __repr__(self):
        return '<Poem (id=%s ' \
               'name=%s ' \
               'general_information_about_the_resource=%s ' \
               'adres_img_for_general_information_about_the_resource=%s ' \
               'date_of_resourc_creation=%s ' \
               'resource_content_date=%s' \
               'publications_per_day=%s' \
               'the_main_focus_of_the_channel=%s' \
               'related_areas=%s' \
               'channel_content=%s' \
               'views=%s' \
               'name_administrator=%s' \
               'other=%s)>' % (self.id,
                               self.name,
                               self.general_information_about_the_resource,
                               self.adres_img_for_general_information_about_the_resource,
                               self.date_of_resourc_creation,
                               self.resource_content_date,
                               self.publications_per_day,
                               self.the_main_focus_of_the_channel,
                               self.related_areas,
                               self.channel_content,
                               self.views,
                               self.name_administrator,
                               self.other,
                               )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
