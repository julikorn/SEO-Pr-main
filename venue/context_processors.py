import datetime
from django.conf import settings
from .models import Hall

def site_info(request):
    promo = settings.PROMO
    promo_active = datetime.date.today() <= datetime.date.fromisoformat(promo["until"])
    return {
        "site": settings.SITE_INFO,
        "nav_halls": Hall.objects.filter(is_active=True),
        "promo": promo if promo_active else None,
    }
