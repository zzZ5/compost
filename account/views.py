from django.shortcuts import render, redirect
from django.db.models import Q
import datetime
import hashlib
from account import forms
from account.models import User, ConfirmString
from django.conf import settings


def _hash_code(s, salt='zzZ5'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def _make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = _hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code


def _send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自苏州有机循环研究院的注册确认邮件'
    text_content = '''感谢注册账号，这里是苏州有机循环研究院堆肥站点，专注于堆肥！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册<a href="http://{}/account/confirm/?code={}" target=blank>请点击该连接</a>，\
                    完成注册！</p>
                    <p>请点击链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
    created_time = confirm.created_time
    now = datetime.datetime.now()
    if now > created_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
    else:
        confirm.user.confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
    content = {'message': message}
    return render(request, 'account/confirm.html', content)


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    content = {'session': request.session}
    return render(request, 'account/index.html', content)


def changepassword(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')


def login(request):
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
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['email'] = user.email
                    return redirect('/account/')
                else:
                    message = '密码错误！'
    content = {'message': message}
    return render(request, 'account/login.html', content)


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    request.session.flush()
    return redirect("/account/login/")


def register(request):
    message = ""
    if request.session.get('is_login', None):
        return redirect('/account/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        message = "请检查填写的内容！"
        if password1 != password2:
            message = '两次输入的密码不同！'
        elif len(password1) < 8:
            message = '密码长度不能小于8位！'
        elif len(password1) > 16:
            message = '密码长度不能大于16位！'
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
    content = {'captcha_form': captcha_form, 'message': message}

    return render(request, 'account/register.html', content)
