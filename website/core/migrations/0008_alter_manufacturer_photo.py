# Generated by Django 5.0.2 on 2024-03-07 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_users_address_remove_users_mailing_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='photo',
            field=models.ImageField(upload_to='img_category/%Y/%m/%d/', verbose_name='Фотография'),
        ),
    ]
