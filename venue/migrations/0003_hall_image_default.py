from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0002_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='image',
            field=models.CharField(default='img/hall-depo.jpg', max_length=200, verbose_name='Картинка (путь в static)'),
        ),
    ]
