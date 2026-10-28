FROM python:3.12-slim AS web

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_STATIC_MANIFEST=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN DJANGO_SECRET_KEY=build-only-not-secret DJANGO_DEBUG=0 \
    python manage.py collectstatic --noinput

RUN useradd --uid 1000 --no-create-home app
USER app

EXPOSE 8000
ENTRYPOINT ["sh", "/app/docker/entrypoint.sh"]
CMD ["gunicorn", "podzemka.wsgi:application", "-c", "/app/docker/gunicorn.conf.py"]

FROM nginx:1.27-alpine AS nginx
COPY --from=web /app/staticfiles /usr/share/nginx/static
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY docker/nginx/security-headers.conf /etc/nginx/snippets/security-headers.conf
COPY docker/nginx/50x.html /usr/share/nginx/html/50x.html