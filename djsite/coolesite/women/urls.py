from django.urls import path, re_path
from .views import *
urlpatterns = [
    path('', index, name='home'), # соответсвует маршруту http://127.0.0.1:8000/
    path('categs/<slug:categ>/', categories), # http://127.0.0.1:8000/categs/
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
