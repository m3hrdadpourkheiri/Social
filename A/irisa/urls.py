from django.urls import path
from . import views

app_name = 'irisa'
urlpatterns=[
    path('main/',views.HomeView.as_view(),name='main')
]
