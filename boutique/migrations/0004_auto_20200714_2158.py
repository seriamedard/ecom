# Generated by Django 2.2 on 2020-07-14 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0003_auto_20200714_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='slug',
            field=models.SlugField(max_length=150, null=True),
        ),
    ]
