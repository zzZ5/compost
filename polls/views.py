from django.shortcuts import render, redirect


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    content = {'session': request.session, 'page_home': True}
    return render(request, 'polls/index.html', content)


def about(request):
    detail = {'title': '关于我们', 'content': '测试文本，测试远程服务器'}
    content = {'detail': detail,
               'session': request.session, 'page_about': True}
    return render(request, 'polls/about.html', content)


def all_equipment(request):
    return


def my_equipment(request):
    return


def list_history(request):
    return


def add_equipment(request):
    return
