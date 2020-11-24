from django.shortcuts import render, redirect, HttpResponse
import random
import hashlib
import time
from django.conf import settings
from polls.models import Equipment
import datetime


def _send_email(email, equipment):
    """
    发送确认邮箱邮件

    Parameter:
        email(string): 要发送邮件的对象
        equipment(equipment): 新注册的设备

    Return:
        None
    """
    from django.core.mail import EmailMultiAlternatives
    subject = '来自苏州有机循环研究院的设备key邮件'
    text_content = '''感谢申请设备key，这里是苏州有机循环研究院堆肥站点，专注于堆肥！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢申请设备”{}“</p>
                    <p>您的key为：<b>{}</b></p>
                    <p>请妥善保存该key。</p>
                    <p>设备描述：{}</p>
                    '''.format(equipment.name, equipment.key, equipment.descript)
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def _get_random_secret_key(length=15, allowed_chars=None, secret_key=None):
    """
    生成随机字符串
    Parameter:
        length(int): 随机字符串长度
        allowed_chars(string): 随机字符串字符取值范围
        secret_key(string): 生成随机字符串的随机字符串
    Return:
        string: 随机生成的字符串
    """
    if allowed_chars is None:
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if secret_key is None:
        secret_key = "n&^-9#k*-6pwzsjt-qsc@s3$l46k(7e%f80e7gx^f#vouf3yvz"

    random.seed(
        hashlib.sha256(
            ("%s%s%s" % (
                random.getstate(),
                time.time(),
                secret_key)).encode('utf-8')
        ).digest())
    ret = ''.join(random.choice(allowed_chars) for i in range(length))
    return ret


def _get_equipment_info(equipment, data_num=3):
    if data_num < 0:
        datas = equipment.data_set.all()
    else:
        datas = equipment.data_set.all()[:data_num]
    interval = ''
    if datas[0]:
        d1 = datas[0].created_time
        d2 = datetime.datetime.now()
        d = d2 - d1
        days = d.days
        mins = d.seconds % 60
        hours = d.seconds // 3600
        interval = '{}天{}小时{}分钟'.format(days, hours, mins)
    info = {'name': equipment.name, 'descript': equipment.descript,
            'datas': datas, 'interval': interval}
    return info


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    equments = [_get_equipment_info(equipment)
                for equipment in Equipment.objects.all()]
    content = {'equipments': equments, 'session': request.session,
               'page_home': True, 'page_allEquipment': True}
    return render(request, 'polls/index.html', content)


def about(request):
    detail = {'title': '关于我们', 'content': '测试文本，测试远程服务器'}
    content = {'detail': detail,
               'session': request.session, 'page_about': True}
    return render(request, 'polls/about.html', content)


def all_equipment(request):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')

    equments = [_get_equipment_info(equipment)
                for equipment in Equipment.objects.all()]
    content = {'equipments': equments}
    return render(request, 'polls/index_allEquipment.html', content)


def my_equipment(request):
    return


def list_history(request):
    return


def create_equipment(request):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')

    message = ''
    if request.method == "POST":
        name = request.POST.get('name')
        descript = request.POST.get('descript')
        same_name = Equipment.objects.filter(name=name)
        if same_name:
            message = '设备名已经存在!'
        elif not name:
            message = '设备名不能为空'
        elif len(name) > 128:
            message = '设备名不能超过128个字符!'
        elif len(descript) > 256:
            message = '设备描述不能超过256个字符!'
        else:
            new_equipment = Equipment()
            new_equipment.name = name
            new_equipment.descript = descript
            # 确保唯一key
            key = _get_random_secret_key()
            while Equipment.objects.filter(key=key):
                key = _get_random_secret_key()
            new_equipment.key = key
            new_equipment.save()
            _send_email(request.session.get('email', None), new_equipment)
            message = '申请成功，请检查邮箱是否收到邮件(若未收到邮件请联系管理员)。'

    content = {'page_createEquipment': True, 'message': message}
    return render(request, 'polls/index_createEquipment.html', content)


def submit(request):
    return


def add_equipment(request):
    return HttpResponse('ok')
