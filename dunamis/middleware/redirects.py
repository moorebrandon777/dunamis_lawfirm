from django.http import HttpResponsePermanentRedirect

class ForceWWWAndHTTPSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        path = request.get_full_path()

        # If not HTTPS or host does not start with www., redirect to https://www.dunamislawfirm.com
        if not request.is_secure() or not host.startswith('www.'):
            new_url = f'https://www.dunamislawfirm.com{path}'
            return HttpResponsePermanentRedirect(new_url)

        return self.get_response(request)

