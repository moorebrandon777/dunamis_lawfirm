from .models import Service

def services_footer(request):
    return {
        'footer_services': Service.objects.all()
    }