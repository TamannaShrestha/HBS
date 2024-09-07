# Generated by Django 5.0 on 2024-08-09 15:37

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0007_hotel_description_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='rating',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(default='pokhara', max_length=100)),
                ('date', models.DateTimeField(default=datetime.datetime(2024, 8, 9, 21, 22, 49, 40974))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('amount', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=200)),
                ('created_date', models.DateField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.order')),
            ],
        ),
    ]
