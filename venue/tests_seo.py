import json
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from .models import Hall, Poster
from .tests import SiteTestCase

STATIC_PAGES = ["home", "hall_list", "menu", "events", "poster_list", "gallery", "contacts"]
SERVICE_PATHS = ["/booking/", "/home/", "/healthz/", "/admin/"]
HEADING = re.compile(r"^h[1-6]$")

class SeoTestCase(SiteTestCase):
    def pages(self):
        response = self.client.get("/sitemap.xml")
        if response.status_code == 200:
            locs = re.findall(r"<loc>(.*?)</loc>", response.content.decode())
            return [urlparse(loc).path for loc in locs]
        paths = [reverse(f"venue:{name}") for name in STATIC_PAGES]
        paths += [h.get_absolute_url() for h in Hall.objects.filter(is_active=True)]
        paths += [p.get_absolute_url() for p in Poster.objects.all()]
        return paths

    def soup(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, f"{path} отдаёт {response.status_code}")
        return BeautifulSoup(response.content, "html.parser")

class SitemapRobotsTest(SeoTestCase):
    def test_sitemap_exists(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200, "Нет /sitemap.xml")
        self.assertIn("xml", response["Content-Type"])

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200, "Нет /robots.txt")
        self.assertTrue(response["Content-Type"].startswith("text/plain"))
        text = response.content.decode()
        self.assertRegex(text, r"(?m)^Sitemap:\s*https?://\S+/sitemap\.xml", "Нет абсолютного Sitemap:")
        self.assertRegex(text, r"(?m)^Disallow:\s*/admin/")

class MetaTagsTest(SeoTestCase):
    def test_html_lang(self):
        html = self.soup("/").find("html")
        self.assertEqual(html.get("lang"), "ru")

    def test_one_h1_on_every_page(self):
        for path in self.pages():
            with self.subTest(path=path):
                h1 = self.soup(path).find_all("h1")
                self.assertEqual(len(h1), 1, f"На странице {len(h1)} шт. <h1>")

    def test_canonical_absolute_and_self(self):
        domain = settings.SITE_INFO["domain"]
        for path in self.pages():
            with self.subTest(path=path):
                tag = self.soup(path).find("link", rel="canonical")
                self.assertIsNotNone(tag, "Нет canonical")
                url = urlparse(tag["href"])
                self.assertIn(url.scheme, ("http", "https"), "canonical не абсолютный")
                self.assertEqual(url.path, path)

    def test_booking_is_noindex(self):
        tag = self.soup("/booking/").find("meta", attrs={"name": "robots"})
        self.assertIsNotNone(tag, "На /booking/ нет meta robots")
        self.assertIn("noindex", tag["content"])

class RedirectsAnd404Test(SeoTestCase):
    def test_home_duplicate_redirects(self):
        self.assertRedirects(self.client.get("/home/"), "/", status_code=301)

    def test_old_hall_urls_redirect_to_slug(self):
        for hall in Hall.objects.filter(is_active=True):
            with self.subTest(hall=hall.name):
                new_url = hall.get_absolute_url()
                response = self.client.get(f"/halls/{hall.pk}/")
                self.assertRedirects(response, new_url, status_code=301)

class ImagesAndMarkupTest(SeoTestCase):
    def test_images_have_alt_and_size(self):
        for path in self.pages():
            for img in self.soup(path).find_all("img"):
                with self.subTest(path=path, src=img.get("src")):
                    self.assertTrue(img.get("alt", "").strip(), "Пустой alt")
                    self.assertTrue(img.get("width") and img.get("height"), "Нет width/height")

    def test_json_ld(self):
        expected = {"/": {"EventVenue", "FAQPage"}}
        for path, types in expected.items():
            with self.subTest(path=path):
                found = set()
                for script in self.soup(path).find_all("script", type="application/ld+json"):
                    data = json.loads(script.string)
                    items = data if isinstance(data, list) else data.get("@graph", [data])
                    found |= {item.get("@type") for item in items}
                self.assertTrue(types <= found, f"Нет разметки: {types - found}")