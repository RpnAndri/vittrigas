# Generated by Django 5.2.1 on 2025-05-15 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(default='products/tree.png', upload_to='products/'),
        ),
    ]
