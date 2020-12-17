from django.shortcuts import render


def index(request):
    content = {'session': request.session, 'page_charts': True, }
    return render(request, 'charts/index.html', content)
