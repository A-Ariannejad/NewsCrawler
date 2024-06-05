# Generated by Django 5.0.6 on 2024-06-04 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomNews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customnew',
            name='status',
            field=models.CharField(choices=[('latest', 'service'), ('most_visited', 'person_to_site')], default='latest', max_length=20),
        ),
    ]