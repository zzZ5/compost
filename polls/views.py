from django.shortcuts import render, redirect


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    content = {'session': request.session}
    return render(request, 'polls/index.html', content)


def about(request):
    detail = {'title': '关于我们', 'content': '测试文本，测试远程服务器'}
    content = {'detail': detail, 'session': request.session}
    return render(request, 'polls/about.html', content)
