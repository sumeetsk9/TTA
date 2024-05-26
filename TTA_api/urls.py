from TTA_api import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", csrf_exempt(views.homepage), name = "homepage"),
    path('TTA', views.TTA, name='TTA')

]