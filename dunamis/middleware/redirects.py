from django.http import HttpResponsePermanentRedirect

class ForceWWWAndHTTPSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        is_secure = request.is_secure()
        path = request.get_full_path()

        # Redirect if not HTTPS or not www
        if not is_secure or not host.startswith('www.'):
            new_url = f'https://www.dunamislawfirm.com{path}'
            return HttpResponsePermanentRedirect(new_url)

        return self.get_response(request)
