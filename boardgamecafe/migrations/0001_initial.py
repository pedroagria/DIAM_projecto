# Generated by Django 4.2.1 on 2023-05-10 18:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoardGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('release_year', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3000)])),
                ('min_players', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('max_players', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('min_age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('min_playing_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('avg_playing_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('complexity', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('number_of_copies', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField()),
                ('link', models.URLField()),
                ('image', models.ImageField(upload_to='')),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('value_paid', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_paid', models.BooleanField()),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.boardgame')),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=50)),
                ('chosen_title', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('vat', models.IntegerField()),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="O número deverá ter o formato: '+3512199999'", regex='^\\?1?\\d{8,15}$')])),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('stock_quantity', models.IntegerField()),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('unlock_conditions', models.TextField()),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('text', models.TextField()),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.boardgame')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='unlocked_titles',
            field=models.ManyToManyField(related_name='people', to='boardgamecafe.title'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_preorder', models.BooleanField()),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.booking')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.product')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.boardgame')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.person')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='calendar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.calendar'),
        ),
        migrations.AddField(
            model_name='booking',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.person'),
        ),
        migrations.AddField(
            model_name='booking',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.table'),
        ),
    ]
