from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0005_hall_meta_description_hall_meta_title_hall_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='slug',
            field=models.SlugField(blank=True, help_text='Человекопонятный URL, например: depo, tonnel, platforma', max_length=120, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='poster',
            name='slug',
            field=models.SlugField(blank=True, help_text='Человекопонятный URL, например: kviz-60-sekund', max_length=150, unique=True, verbose_name='URL'),
        ),
    ]
