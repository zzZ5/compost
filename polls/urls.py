from django.urls import path, include
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('allEquipment/', views.all_equipment, name='all_equipment'),
    path('myEquipment/', views.index, name='my_equipment'),
    path('addEquipment/', views.index, name='add_equipment'),
    path('listHistory', views.index, name='list_history'),
]
