from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from frontend.sitemaps import StaticViewSitemap, AttorneySitemap, ServiceSitemap


sitemaps = {
    'static': StaticViewSitemap,
    'attorneys': AttorneySitemap,
    'services': ServiceSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('captcha/', include('captcha.urls')),
]
