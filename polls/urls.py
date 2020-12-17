from django.urls import path, include
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('all_equipment/', views.all_equipment, name='all_equipment'),
    path('my_equipment/', views.my_equipment, name='my_equipment'),
    path('draw_chart/', views.draw_chart, name='draw_chart'),
    path('create_equipment/', views.create_equipment, name='create_equipment'),
    path('list_history/', views.list_history, name='list_history'),
    path('submit/', views.submit, name='submit'),
    path('add_equipment/', views.add_equipment, name='add_equipment'),
    path('get_server_info/', views.get_server_info, name='get_server_info'),
]
