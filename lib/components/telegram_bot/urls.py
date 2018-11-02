from django.urls import path

def test(request):
    pass

urlpatterns = [
    path('test/',    test),
    path('test2/',   test),
]
