from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0004_poster_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='hall',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='hall',
            name='meta_title',
            field=models.CharField(blank=True, max_length=70, verbose_name='Meta Title'),
        ),
        migrations.AddField(
            model_name='hall',
            name='slug',
            field=models.SlugField(blank=True, help_text='Человекопонятный URL, например: depo, tonnel, platforma', max_length=120, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='poster',
            name='slug',
            field=models.SlugField(blank=True, help_text='Человекопонятный URL, например: kviz-60-sekund', max_length=150, verbose_name='URL'),
        ),
    ]
