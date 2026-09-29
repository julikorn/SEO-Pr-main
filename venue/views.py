import datetime
from django.contrib import messages
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BookingForm
from .models import FAQ, EventFormat, Hall, MenuPackage, Poster, Review

def home(request):
    reviews = Review.objects.filter(is_published=True)
    context = {
        "halls": Hall.objects.filter(is_active=True),
        "formats": EventFormat.objects.all()[:6],
        "packages": MenuPackage.objects.filter(is_featured=True)[:3],
        "reviews": reviews[:6],
        "rating": reviews.aggregate(avg=Avg("rating"))["avg"],
        "reviews_count": reviews.count(),
        "faqs": FAQ.objects.all(),
        "posters": upcoming_posters()[:6],
        "form": BookingForm(),
    }
    return render(request, "venue/home.html", context)

def hall_list(request):
    return render(request, "venue/hall_list.html", {
        "halls": Hall.objects.filter(is_active=True),
    })

def hall_detail(request, slug):
    hall = get_object_or_404(Hall, slug=slug, is_active=True)
    others = Hall.objects.filter(is_active=True).exclude(pk=hall.pk)
    form = BookingForm(initial={"hall": hall})
    return render(request, "venue/hall_detail.html", {
        "hall": hall,
        "others": others,
        "form": form,
    })

def hall_detail_redirect(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    return redirect("venue:hall_detail", slug=hall.slug, permanent=True)

def upcoming_posters():
    return Poster.objects.filter(is_published=True).filter(
        Q(date__gte=datetime.date.today()) | ~Q(schedule=""),
    )

def poster_list(request):
    return render(request, "venue/poster_list.html", {
        "posters": upcoming_posters(),
    })

def poster_detail(request, slug):
    poster = get_object_or_404(Poster, slug=slug, is_published=True)
    return render(request, "venue/poster_detail.html", {
        "poster": poster,
        "is_past": not poster.schedule and poster.date < datetime.date.today(),
    })

def poster_detail_redirect(request, pk):
    poster = get_object_or_404(Poster, pk=pk)
    return redirect("venue:poster_detail", slug=poster.slug, permanent=True)

def menu(request):
    return render(request, "venue/menu.html", {
        "packages": MenuPackage.objects.all(),
    })

def events(request):
    return render(request, "venue/events.html", {
        "formats": EventFormat.objects.all(),
        "halls": Hall.objects.filter(is_active=True),
    })

def gallery(request):
    photos = [
        {"src": "img/hall-depo.jpg", "caption": "Зал «Депо»"},
        {"src": "img/hall-tonnel.webp", "caption": "Зал «Тоннель»"},
        {"src": "img/hall-platforma.jpg", "caption": "Зал «Платформа»"},
        {"src": "img/hall-vestibul.jpg", "caption": "Бар «Вестибюль»"},
    ]
    return render(request, "venue/gallery.html", {"photos": photos})

def contacts(request):
    return render(request, "venue/contacts.html")

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка принята! Перезвоним в течение 15 минут.")
            return redirect("venue:booking")
    else:
        form = BookingForm(initial={
            "hall": request.GET.get("hall"),
            "comment": request.GET.get("comment", ""),
            "guests": request.GET.get("guests"),
        })
    return render(request, "venue/booking.html", {"form": form})