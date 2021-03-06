# Generated by Django 4.0.1 on 2022-01-22 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0006_remove_post_fecha_ultima_modificacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('nombre_usuario', models.CharField(max_length=30)),
                ('apellido_usuario', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('profesion', models.CharField(max_length=30)),
                ('edad', models.DecimalField(decimal_places=0, max_digits=3)),
            ],
        ),
    ]
