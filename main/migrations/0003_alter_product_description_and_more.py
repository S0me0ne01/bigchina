# Generated by Django 4.1.6 on 2023-08-10 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_name_kg_category_name_kz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_kz',
            field=models.TextField(blank=True, null=True),
        ),
    ]