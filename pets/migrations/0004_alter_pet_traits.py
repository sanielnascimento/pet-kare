# Generated by Django 4.2 on 2023-04-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0003_remove_trait_pets'),
        ('pets', '0003_alter_pet_traits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='traits',
            field=models.ManyToManyField(related_name='pets', to='traits.trait'),
        ),
    ]
