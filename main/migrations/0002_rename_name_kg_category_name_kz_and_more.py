# Generated by Django 4.1.6 on 2023-08-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name_kg',
            new_name='name_kz',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='name_kg',
            new_name='name_kz',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description_kg',
            new_name='description_kz',
        ),
        migrations.RenameField(
            model_name='visit',
            old_name='from_kg',
            new_name='from_kz',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name_kg',
        ),
        migrations.AddField(
            model_name='product',
            name='name_kz',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default=0, max_length=10000),
            preserve_default=False,
        ),
    ]
