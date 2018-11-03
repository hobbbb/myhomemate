import importlib

from django.urls import path, include

# from components.utils import get_urls_modules
from myhome import views

urlpatterns = [
    path('components/',                 views.component_list, name='components'),
    path('components/<str:filt>/',      views.component_list, name='components_filt'),
    path('components/<int:id>/',        views.component_setup),
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
