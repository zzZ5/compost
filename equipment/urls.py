from django.urls import path, include
from . import views

app_name = 'equipment'
urlpatterns = [
    path('', views.index, name='index'),
    path('datas/<name>/', views.list_data, name='list_data'),
]
