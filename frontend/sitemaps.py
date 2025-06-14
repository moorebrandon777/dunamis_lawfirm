from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Attorney, Service

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home', 'attorneys_list', 'about']

    def location(self, item):
        return reverse(f'frontend:{item}')


class AttorneySitemap(Sitemap):
    def items(self):
        return Attorney.objects.all()

    def location(self, obj):
        return reverse('frontend:attorney_detail', args=[obj.slug])
    

class ServiceSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return reverse('frontend:service_detail', args=[obj.slug])
