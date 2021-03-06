from django.urls import path, include
from . import views

app_name = 'equipment'
urlpatterns = [
    path('<id>/', views.index, name='index'),
    path('<id>/datas/', views.list_data, name='list_data'),
    path('<id>/modify_equipment/', views.modify_equipment, name='modify_equipment'),
    path('<id>/download/', views.download_data, name='download_data'),
    path('<id>/get_equipment_data/',
         views.get_equipment_data, name='get_equipment_data')
]
