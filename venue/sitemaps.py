from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Hall

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "venue:home",
            "venue:hall_list",
            "venue:poster_list",
            "venue:menu",
            "venue:events",
            "venue:gallery",
            "venue:contacts",
        ]

    def location(self, item):
        return reverse(item)

class HallSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Hall.objects.filter(is_active=True)