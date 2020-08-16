# Generated by Django 3.0.8 on 2020-08-16 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dash_app', '0002_quote_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_quotes', to='dash_app.User'),
        ),
    ]
