from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    url_name = 'layout-home'
    template_name = 'layout/home.html'


def permission_denied403(request, exception):
    data = {
        'status_code': 403,
        'message': 'Permission Denied',
    }
    return render(request, 'layout/error.html', data)


def not_found404(request, exception):
    data = {
        'status_code': 404,
        'message': 'Not Found',
    }
    return render(request, 'layout/error.html', data)


def server_error500(request):
    data = {
        'status_code': 500,
        'message': 'Internal Server Error',
    }
    return render(request, 'layout/error.html', data)
