# Generated by Django 3.2 on 2022-01-28 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0009_auto_20220128_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image_post',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post_app.post', verbose_name='Post'),
        ),
    ]
