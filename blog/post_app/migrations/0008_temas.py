# Generated by Django 4.0.1 on 2022-01-25 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0007_usuarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=30)),
            ],
        ),
    ]
