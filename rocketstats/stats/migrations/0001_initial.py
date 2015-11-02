# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RLRatings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mt_1v1', models.IntegerField()),
                ('mt_2v2', models.IntegerField()),
                ('mt_3v3_solo', models.IntegerField()),
                ('mt_3v3', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RLRatingsHistorical',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mt_1v1', models.IntegerField()),
                ('mt_2v2', models.IntegerField()),
                ('mt_3v3_solo', models.IntegerField()),
                ('mt_3v3', models.IntegerField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RLSkills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wins', models.IntegerField()),
                ('goals', models.IntegerField()),
                ('mvps', models.IntegerField()),
                ('saves', models.IntegerField()),
                ('shots', models.IntegerField()),
                ('assists', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RLSkillsHistorical',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wins', models.IntegerField()),
                ('goals', models.IntegerField()),
                ('mvps', models.IntegerField()),
                ('saves', models.IntegerField()),
                ('shots', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RLUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=75)),
                ('network', models.CharField(max_length=3, choices=[(b'S', b'Steam'), (b'PSN', b'Playstation Network')])),
                ('network_id', models.BigIntegerField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='rlskillshistorical',
            name='user',
            field=models.ForeignKey(to='stats.RLUser'),
        ),
        migrations.AddField(
            model_name='rlskills',
            name='user',
            field=models.OneToOneField(to='stats.RLUser'),
        ),
        migrations.AddField(
            model_name='rlratingshistorical',
            name='user',
            field=models.ForeignKey(to='stats.RLUser'),
        ),
        migrations.AddField(
            model_name='rlratings',
            name='user',
            field=models.OneToOneField(to='stats.RLUser'),
        ),
    ]
