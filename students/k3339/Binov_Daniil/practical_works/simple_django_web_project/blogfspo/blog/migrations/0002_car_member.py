# Generated by Django 4.2.16 on 2024-11-03 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='member',
            field=models.ManyToManyField(through='blog.Ownership', to='blog.owner'),
        ),
    ]
