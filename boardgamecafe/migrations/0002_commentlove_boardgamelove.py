# Generated by Django 4.2.1 on 2023-05-11 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boardgamecafe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.comment')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.person')),
            ],
        ),
        migrations.CreateModel(
            name='BoardGameLove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_is_active', models.BooleanField()),
                ('log_date_created', models.DateTimeField()),
                ('log_date_last_update', models.DateTimeField()),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.boardgame')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boardgamecafe.person')),
            ],
        ),
    ]
