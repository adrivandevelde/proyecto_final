# Generated by Django 3.2 on 2022-01-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0003_rename_fecha_publicación_post_fecha_publicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='fecha_publicacion',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Publicaión'),
        ),
        migrations.AlterField(
            model_name='post',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Titulo'),
        ),
    ]
