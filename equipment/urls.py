from django.urls import path, include
from . import views

app_name = 'equipment'
urlpatterns = [
    path('<id>', views.index, name='index'),
    path('<id>/datas', views.list_data, name='list_data'),
]
