from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from . import views

urlpatterns = [
    path("", csrf_exempt(views.main_view_json), name='main_view'),
    path("quport/<str:token>/", csrf_exempt(views.api_support), name='api_support'),
]
