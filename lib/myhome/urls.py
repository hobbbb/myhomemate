import importlib

from django.urls import path, include, re_path

# from components.utils import get_urls_modules
from myhome import views

urlpatterns = [
    path('',                            views.main, name='main'),
    path('components/',                 views.component_list, name='act_components'),
    path('components/all/',             views.component_list, {'filt': 'all'}, name='all_components'),
    path('components/edit/<int:id>/',   views.component_edit, name='component_edit'),
    path('devices/',                    views.device_list, name='device_list'),
    path('devices/edit/<int:id>/',      views.device_edit, name='device_edit'),
    path('zones/',                      views.zone_list, name='zone_list'),
    path('zones/edit/',                 views.zone_edit, name='zone_new'),
    path('zones/edit/<int:id>/',        views.zone_edit, name='zone_edit'),
    path('persons/',                    views.person_list, name='person_list'),
    path('persons/edit/',               views.person_edit, name='person_new'),
    path('persons/edit/<int:id>/',      views.person_edit, name='person_edit'),
    path('rooms/',                      views.room_list, name='room_list'),
    path('rooms/edit/',                 views.room_edit, name='room_new'),
    path('rooms/edit/<int:id>/',        views.room_edit, name='room_edit'),
    path('automations/',                views.automation_list, name='automation_list'),
    path('automations/<int:id>/',       views.automation_edit, name='automation_edit'),
    path('logs/',                       views.log_list, name='log_list'),
    path('map/',                        views.map, name='map'),
]


# for c, m in get_urls_modules():
#     try:
#         importlib.import_module(m)
#     except ModuleNotFoundError:
#         continue

#     # from components.telegram_bot.urls import urlpatterns as component_urls
#     # urlpatterns.append(
#     #     path('component/{}/'.format(c), include(component_urls))
#     # )
#     # print(m)
