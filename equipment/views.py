import codecs
import csv
import datetime
import json
import time

from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from django.shortcuts import render, Http404, redirect, HttpResponse
from polls.models import Equipment, Data
from account.models import User

from pyecharts.charts import Line
import pyecharts.options as opts

every_page_data = 100


def index(request, id):
    """
    设备主页
    """
    if not request.session.get('is_login', None):
        return redirect('/account/login/')

    uid = request.session.get('uid', None)
    user = User.objects.filter(id=uid)[
        0] if User.objects.filter(id=uid) else None

    equipment = Equipment.objects.filter(
        id=id)[0] if Equipment.objects.filter(id=id) else None

    if not equipment:
        return Http404

    datas = equipment.data_set.all()[:100][::-1]
    dates = list(data.created_time.strftime('%Y-%m-%d %H:%M:%S')
                 for data in datas)
    values = list(data.value for data in datas)
    line = Line()
    line.add_xaxis(dates)
    line.add_yaxis(equipment.name, values, symbol_size=5,
                   is_hover_animation=False,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(width=1.5),
                   is_smooth=True)
    line.set_global_opts(
        toolbox_opts=opts.ToolboxOpts(True,   feature={
            "dataZoom": {"yAxisIndex": "none"},
            "restore": {},
            "saveAsImage": {},
            "dataView": {}

        },),
        yaxis_opts=opts.AxisOpts(name='最新100条数据'),
        tooltip_opts=opts.TooltipOpts(True, trigger="axis"),
        datazoom_opts=opts.DataZoomOpts(True, range_start=0, range_end=100)
    )
    is_admin = user.admin
    content = {'linechart_recent_data': line.dump_options(),
               'equipment': equipment,
               'session': request.session, 'page_equipment': True, 'admin': is_admin}
    return render(request, 'equipment/index.html', content)


def modify_equipment(request, id):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')

    uid = request.session.get('uid', None)
    user = User.objects.filter(id=uid)[
        0] if User.objects.filter(id=uid) else None

    equipment = Equipment.objects.filter(
        id=id)[0] if Equipment.objects.filter(id=id) else None

    response = {
        'Code': 0,
        'Message': '未知错误！'
    }

    if not equipment:
        response['Code'] = 111
        response['Message'] = '未找到该设备！'
        return HttpResponse(json.dumps(response))

    if request.method == 'GET':
        name = request.GET.get('name', None)
        descript = request.GET.get('descript', None)
        is_changed = True
        if name != equipment.name:
            if Equipment.objects.filter(name=name):
                response['Code'] = 112
                response['Message'] = '该设备已存在！'
                is_changed = False
            elif not user.admin:
                response['Code'] = 102
                response['Message'] = '权限不足！'
                is_changed = False
        if is_changed:
            equipment.name = name
            equipment.descript = descript
            equipment.save()
            response['Code'] = 100
            response['Message'] = '保存成功！'
    return HttpResponse(json.dumps(response))


def list_data(request, id):
    """/;
    数据页面
    """

    if not request.session.get('is_login', None):
        return redirect('/account/login/')

    uid = request.session.get('uid', None)
    user = User.objects.filter(id=uid)[
        0] if User.objects.filter(id=uid) else None

    equipment = Equipment.objects.filter(
        id=id)[0] if Equipment.objects.filter(id=id) else None

    if not equipment:
        return Http404

    if request.method == 'POST' and user.admin:
        del_list = request.POST.getlist('checkbox_data')
        Data.objects.filter(id__in=del_list).delete()

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
    if user.admin:
        return render(request, 'equipment/page_list_data_admin.html', content)
    else:
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


def get_equipment_data(request, id):

    response = {
        'Code': 0,
        'Message': '未知错误！',
        'Action': '',
        'Data': ''
    }

    if request.method == 'GET':
        action = request.GET.get('action', None)
        datas = []
        print(action)
        equipment = Equipment.objects.filter(
            id=id)[0] if Equipment.objects.filter(id=id) else None
        if action == 'day':
            datas = equipment.data_set.filter(
                created_time__gt=(datetime.datetime.now() + datetime.timedelta(days=-1)))
        elif action == 'three_day':
            datas = equipment.data_set.filter(
                created_time__gt=(datetime.datetime.now() + datetime.timedelta(days=-3)))
        elif action == 'month':
            datas = equipment.data_set.filter(
                created_time__gt=(datetime.datetime.now() + datetime.timedelta(days=-30)))
        elif action == 'three_month':
            datas = equipment.data_set.filter(
                created_time__gt=(datetime.datetime.now() + datetime.timedelta(days=-90)))
        elif action == 'all':
            datas = equipment.data_set.all()
        response['Code'] = 100
        response['Message'] = '获取数据成功！'
        response['Data'] = list({'name': data.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 'value': [data.created_time.strftime('%Y-%m-%d %H:%M:%S'), data.value]} for data in datas)[::-1]
    return HttpResponse(json.dumps(response))
