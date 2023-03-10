# Generated by Django 4.1.6 on 2023-03-01 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0002_pedido_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.UUIDField(default=True, primary_key=True, serialize=False)),
                ('category', models.CharField(default='', max_length=255)),
                ('dish', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Platos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=4)),
                ('img', models.URLField()),
                ('dscr', models.CharField(max_length=100)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='endpoints.categoria')),
            ],
        ),
    ]
