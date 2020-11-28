from django.urls import path
from .views import upload_view, preference_view

urlpatterns = [
    path('pref/', preference_view, name='preference'),
    path('', upload_view, name='upload'),
]