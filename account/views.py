import datetime
import hashlib

from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from account import forms
from account.models import User, ConfirmString

ip = '118.25.108.254:80'


def _makesure_password(pd1, pd2):
    """
    确认两个密码一样且符合规格

    Parameter:
        pd1(string): 密码1
        pd2(string): 密码2

    Return:
        string: 返回提示信息，如果密码正确则返回空
    """
    message = ""
    if pd1 != pd2:
        message = '两次输入的密码不一样！'
    elif len(pd1) < 8:
        message = '密码长度不能小于8位！'
    elif len(pd1) > 16:
        message = '密码长度不能大于16位！'
    return message


def _hash_code(s, salt='zzZ5'):
    """
    加密字符串

    Parameter:
        s(string): 需要加密的字符串
        salt(string): 加密中加的"盐分"

    Return:
        string: 加密后的256位字符串
    """
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def _make_confirm_string(user):
    """
    创建确认码

    Parameter:
        user(models.User): 确认码绑定的用户

    Return:
        string: 该用户的确认码
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = _hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def _send_email(email, code):
    """
    发送确认邮箱邮件

    Parameter:
        email(string): 确认码绑定的用户

    Return:
        None
    """
    from django.core.mail import EmailMultiAlternatives
    subject = '来自苏州有机循环研究院的注册确认邮件'
    text_content = '''感谢注册账号，这里是苏州有机循环研究院堆肥站点，专注于堆肥！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册<a href="http://{}/account/confirm/?code={}" target=blank>请点击该连接</a>，\
                    完成注册！</p>
                    <p>请点击链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(ip, code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    """
    邮箱确认界面
    """
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
    created_time = confirm.created_time
    now = datetime.datetime.now()

    if now > created_time + datetime.timedelta(settings.CONFIRM_DAYS):
        # 确认邮件是否过期，如果过期便删除账号，让用户重新注册
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
    else:
        confirm.user.confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
    content = {'message': message, 'page_confirm': True}
    return render(request, 'account/confirm.html', content)


def index(request):
    """
    账户信息页面
    """
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    message = ''
    if request.method == 'POST':
        uid = request.session.get('uid', None)
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = User.objects.get(id=uid)
        is_changed = True

        if username != user.username:
            if User.objects.filter(username=username):
                message = '该用户名已存在'
                is_changed = False
        if email != user.email:
            if User.objects.filter(email=email):
                message = '该邮箱已经被注册了！'
                is_changed = False
            else:
                code = _make_confirm_string(user)
                user.confirmed = False
                _send_email(email, code)
                message = '邮箱已修改，请前往邮箱进行确认！'
        if is_changed:
            user.username = username
            user.email = email
            user.save()
            request.session['username'] = user.username
            request.session['email'] = user.email
            message = '保存成功！' if message == '' else message

    content = {'message': message,
               'session': request.session, 'page_myaccount': True}
    return render(request, 'account/index.html', content)


def login(request):
    """
    登陆界面
    """
    message = ""
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/account/')

    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        message = "请检查填写的内容！"
        if name.strip() and password:  # 确保用户名和密码都不为空
            try:
                user = User.objects.get(Q(username=name) | Q(email=name))
            except:
                message = "用户名或邮箱不存在!"
            else:
                if not user.confirmed:
                    message = '邮箱未验证！'
                elif user.password == _hash_code(password):
                    request.session['is_login'] = True
                    request.session['uid'] = user.id
                    request.session['username'] = user.username
                    request.session['email'] = user.email
                    return redirect('/')
                else:
                    message = '密码错误！'
    content = {'message': message, 'page_login': True}
    return render(request, 'account/login.html', content)


def logout(request):
    """
    登出命令
    """
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    request.session.flush()
    return redirect("/account/login/")


def change_password(request):
    """
    更改账户密码界面
    """
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    message = ''
    if request.method == "POST":
        uid = request.session.get('uid', None)
        password = request.POST.get('password')
        newpassword1 = request.POST.get('newpassword1')
        newpassword2 = request.POST.get('newpassword2')
        user = User.objects.get(pk=uid)
        if user.password != _hash_code(password):
            message = '密码错误！'
        elif _makesure_password(newpassword1, newpassword2):
            message = _makesure_password(newpassword1, newpassword2)
        else:
            user.password = _hash_code(newpassword1)
            user.save()
            request.session.flush()
            message = '密码已修改，请重新登陆'
            content = {'message': message}
            return render(request, 'account/login.html', content)

    content = {'message': message,
               'session': request.session, 'page_myaccount': True}
    return render(request, 'account/change_password.html', content)


def register(request):
    """
    注册账号界面
    """
    message = ""
    if request.session.get('is_login', None):
        return redirect('/account/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        message = "请检查填写的内容！"
        if _makesure_password(password1, password2):
            message = _makesure_password(password1, password2)
        else:
            same_username = User.objects.filter(username=username)
            same_email = User.objects.filter(email=email)
            if same_username:
                message = '用户名已经存在!'
            elif same_email:
                message = '该邮箱已经被注册了！'
            else:
                new_user = User()
                new_user.username = username
                new_user.email = email
                new_user.password = _hash_code(password1)
                new_user.save()
                code = _make_confirm_string(new_user)
                _send_email(email, code)
                message = '请前往邮箱进行确认！'
                return render(request, 'account/login.html', {'message': message})

    captcha_form = forms.captchaForm(request.POST)
    content = {'captcha_form': captcha_form,
               'message': message, 'page_register': True}

    return render(request, 'account/register.html', content)
