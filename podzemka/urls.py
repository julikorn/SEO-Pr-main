from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from venue.sitemaps import HallSitemap, StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "halls": HallSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"
    )),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("", include("django_prometheus.urls")),
    path("", include("venue.urls")),
]