# Generated by Django 5.0.4 on 2024-05-01 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stylish_analyzer', '0002_alter_lexem_style_alter_lexem_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lexem',
            name='word',
            field=models.TextField(unique=True),
        ),
    ]
