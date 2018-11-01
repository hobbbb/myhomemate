from django.contrib import admin
from django.urls import path

from myhome import views

urlpatterns = [
    path('components/', views.components),

    path('admin/', admin.site.urls),
]
