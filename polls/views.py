from django.shortcuts import render, redirect


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/account/login/')
    content = {'session': request.session}
    return render(request, 'polls/index.html', content)
