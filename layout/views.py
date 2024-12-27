from django.views.generic import TemplateView


class Home(TemplateView):
    url_name = 'layout-home'
    template_name = 'layout/home.html'
    