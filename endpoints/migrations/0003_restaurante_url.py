# Generated by Django 4.1.6 on 2023-02-15 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0002_categoria_restaurante_plato'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurante',
            name='url',
            field=models.URLField(default=''),
        ),
    ]