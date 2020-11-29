from django.shortcuts import render, Http404, redirect, HttpResponse
from polls.models import Equipment
from django.core.paginator import Paginator
import csv
from django.http import StreamingHttpResponse
import codecs
import time

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


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def download_data(request, id):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    if not request.session.get('is_login', None):
        return redirect('/account/login/')

    equipment = Equipment.objects.filter(
        id=id)[0] if Equipment.objects.filter(id=id) else None

    if not equipment:
        return Http404

    datas = equipment.data_set.all()

    rows = ([data.value, data.created_time.strftime('%Y-%m-%d %H:%M:%S')]
            for data in datas)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    writer.writerow(['value', 'created_time'])
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
        equipment.name)
    return response
