import os

from django.core.paginator import Paginator

from .models import Channels


def delete_file(old_adres):
    if os.path.exists(f"TelegramChannels/MadiaTelegramChannels/Channels/{old_adres}"):
        os.remove(f"TelegramChannels/MadiaTelegramChannels/Channels/{old_adres}")


def delete_from_db(result):
    for i in result.items():
        if i[0] != 'csrfmiddlewaretoken':
            if i[0] != 'del':
                person = Channels.objects.get(id=i[1])
                old_adres = person.adres_img_for_general_information_about_the_resource
                Channels.objects.filter(id=i[1]).delete()
                delete_file(old_adres)


def get_our_home_page(request, all_channels):
    paginator = Paginator(all_channels, 15)
    page_number = request.GET.get('page', 1)
    pages = paginator.get_page(page_number)

    is_paginated = pages.has_other_pages()
    if pages.has_previous():
        prev_url = f'?page={pages.previous_page_number()}'
    else:
        prev_url = ''
    if pages.has_next():
        next_url = f'?page={pages.next_page_number()}'
    else:
        next_url = ''
    context = {
        'pages': pages,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
    }
    return context


def add(data):
    Channels.objects.create(name=data['name'],
                            general_information_about_the_resource=data[
                                'general_information_about_the_resource'],
                            adres_img_for_general_information_about_the_resource=data[
                                'adres_img_for_general_information_about_the_resource'],
                            name_administrator=data['name_administrator'],
                            other=data['other'],
                            date_of_resourc_creation=data['date_of_resourc_creation'],
                            resource_content_date=data['resource_content_date'],
                            publications_per_day=data['publications_per_day'],
                            the_main_focus_of_the_channel=data['the_main_focus_of_the_channel'],
                            related_areas=data['related_areas'],
                            channel_content=data['channel_content'],
                            views=data['views'],
                            )


def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
