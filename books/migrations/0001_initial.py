# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-16 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'add_book',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('ATID', models.AutoField(primary_key=True, serialize=False)),
                ('ATTitle', models.CharField(max_length=40)),
                ('ATContent', models.TextField(max_length=2000)),
                ('ATDate', models.DateField()),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('AID', models.AutoField(primary_key=True, serialize=False)),
                ('AName', models.CharField(db_index=True, max_length=50)),
                ('ABirthdate', models.DateField(null=True)),
                ('ANationality', models.CharField(max_length=30)),
                ('ABrief', models.TextField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('BISBN', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('BTitle', models.CharField(db_index=True, max_length=40)),
                ('BPublisher', models.CharField(max_length=20)),
                ('BPrice', models.DecimalField(decimal_places=2, max_digits=6)),
                ('BBrief', models.TextField(blank=True, max_length=300, null=True)),
                ('AID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Author')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('FID', models.AutoField(primary_key=True, serialize=False)),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'favorite',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('GID', models.AutoField(primary_key=True, serialize=False)),
                ('GBuildDate', models.DateField()),
                ('GName', models.CharField(db_index=True, max_length=20)),
                ('GBuilder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Group')),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'join',
            },
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('RID', models.AutoField(primary_key=True, serialize=False)),
                ('RTitle', models.CharField(max_length=40)),
                ('RContent', models.TextField(max_length=2000)),
                ('RDate', models.DateField()),
                ('BID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'remark',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('TID', models.AutoField(primary_key=True, serialize=False)),
                ('Ttype', models.CharField(max_length=10, unique=True)),
                ('Books', models.ManyToManyField(to='books.Book')),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='GID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Group'),
        ),
        migrations.AddField(
            model_name='article',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='addbook',
            name='BID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book'),
        ),
        migrations.AddField(
            model_name='addbook',
            name='FID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Favorite'),
        ),
        migrations.AlterUniqueTogether(
            name='join',
            unique_together=set([('GID', 'UID')]),
        ),
        migrations.AlterUniqueTogether(
            name='addbook',
            unique_together=set([('FID', 'BID')]),
        ),
    ]