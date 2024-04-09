# Generated by Django 4.2.11 on 2024-04-09 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_app', '0005_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='recipe_images/')),
            ],
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')]),
        ),
    ]
