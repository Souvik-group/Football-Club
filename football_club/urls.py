"""
URL configuration for football_club project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.utils import timezone

SITE_URL = 'https://arjungeria-agni-sangha-glvz.onrender.com'

def robots_view(request):
    content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /dashboard/
Disallow: /admin-login/
Disallow: /admin-logout/
Sitemap: {SITE_URL}/sitemap.xml"""
    return HttpResponse(content, content_type='text/plain')

def sitemap_view(request):
    from core.models import News, Event
    urls = [
        {'loc': f'{SITE_URL}/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': f'{SITE_URL}/news/', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': f'{SITE_URL}/events/', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': f'{SITE_URL}/team/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': f'{SITE_URL}/about/', 'priority': '0.6', 'changefreq': 'monthly'},
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += f'  <url><loc>{u["loc"]}</loc><changefreq>{u["changefreq"]}</changefreq><priority>{u["priority"]}</priority></url>\n'
    xml += '</urlset>'
    return HttpResponse(xml, content_type='application/xml')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('robots.txt', robots_view, name='robots'),
    path('sitemap.xml', sitemap_view, name='sitemap'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
