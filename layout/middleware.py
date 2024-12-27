from django.utils.deprecation import MiddlewareMixin


class HTMXMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.base_template = 'layout/fragment.html' if request.htmx else 'layout/base.html'

    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        return response
