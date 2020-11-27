from django.shortcuts import render, Http404
from polls.models import Equipment
from django.core.paginator import Paginator

every_page_data = 100


def index(request):
    """
    设备主页
    """
    content = {'session': request.session, 'page_equipment': True}
    return render(request, 'polls/index.html', content)


def list_data(request, id):
    """
    数据页面
    """

    try:
        equipment = Equipment.objects.filter(
            id=int(id))[0] if Equipment.objects.filter(id=int(id)) else None
    except:
        return Http404

    if not equipment:
        return Http404

    try:
        current_page = int(request.GET.get(
            "page")) if request.GET.get("page") else 1
    except:
        current_page = 1
    paginator = Paginator(equipment.data_set.all(), every_page_data)
    if current_page < 0 or current_page > paginator.num_pages:
        current_page = 1

    content = {'session': request.session, 'equipment': equipment,
               'page_list_data': True, 'datas': paginator.page(current_page), 'paginator': paginator.page(current_page)}
    return render(request, 'equipment/page_list_data.html', content)
