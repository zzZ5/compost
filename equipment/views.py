from django.shortcuts import render, Http404, redirect
from polls.models import Equipment
from django.core.paginator import Paginator

every_page_data = 100


def index(request, id):
    """
    设备主页
    """
    if not request.session.get('is_login', None):
        return redirect('/account/login/')

    equipment = Equipment.objects.filter(
        id=id)[0] if Equipment.objects.filter(id=id) else None

    if not equipment:
        return Http404

    message = ''
    if request.method == 'POST':
        name = request.POST.get('name', None)
        descript = request.POST.get('descript')
        is_changed = True

        if name != equipment.name:
            if Equipment.objects.filter(name=name):
                message = '该设备名已存在'
                is_changed = False

        if is_changed:
            equipment.name = name
            equipment.descript = descript
            equipment.save()
            message = '保存成功！' if message == '' else message

    content = {'equipment': equipment, 'message': message,
               'session': request.session, 'page_equipment': True}
    return render(request, 'equipment/index.html', content)


def list_data(request, id):
    """
    数据页面
    """

    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    equipment = Equipment.objects.filter(
        id=id)[0] if Equipment.objects.filter(id=id) else None

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
