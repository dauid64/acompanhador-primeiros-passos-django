# Generated by Django 5.2.1 on 2025-06-30 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capitulos', '0012_alter_exerciciousuario_dificuldade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercicio',
            name='ordem',
            field=models.IntegerField(default=9252),
        ),
    ]
