from django.urls import path, include
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('allEquipment/', views.all_equipment, name='all_equipment'),
    path('myEquipment/', views.my_equipment, name='my_equipment'),
    path('createEquipment/', views.create_equipment, name='create_equipment'),
    path('listHistory/', views.list_history, name='list_history'),
    path('submit/', views.submit, name='submit'),
    path('addEquipment/', views.add_equipment, name='add_equipment'),
]
