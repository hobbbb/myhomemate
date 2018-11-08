import importlib

from django.urls import path, include

# from components.utils import get_urls_modules
from myhome import views

urlpatterns = [
    path('components/',                 views.component_list, name='act_components'),
    path('components/all/',             views.component_list, {'filt': 'all'}, name='all_components'),
    path('components/<int:id>/',        views.component_setup),
    path('devices/',                    views.device_list, name='device_list'),
    path('devices/<int:id>/',           views.device_setup),
    path('persons/',                    views.person_list, name='person_list'),
    path('persons/<int:id>/',           views.person_setup),
    path('rooms/',                      views.room_list, name='room_list'),
    path('rooms/<int:id>/',             views.room_setup),
    path('zones/',                      views.zone_list, name='zone_list'),
    path('zones/<int:id>/',             views.zone_setup),
    path('automations/',                views.automation_list, name='automation_list'),
    path('automations/<int:id>/',       views.automation_setup, name='automation_setup'),
    path('logs/',                       views.log_list, name='log_list'),
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
