# Generated by Django 3.2 on 2022-01-28 14:36

from django.db import migrations, models
import django.db.models.deletion
import post_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0008_temas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='fecha_publicacion',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Publicación'),
        ),
        migrations.CreateModel(
            name='Image_Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=post_app.models.post_image_paht)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post_app.post', verbose_name='Psot')),
            ],
        ),
    ]