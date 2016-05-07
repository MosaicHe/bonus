# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-07 06:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BonusCountDay',
            fields=[
                ('consumer', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('count_num', models.IntegerField(default=0)),
                ('other_info', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BonusCountMonth',
            fields=[
                ('consumer', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('count_num', models.IntegerField(default=0)),
                ('other_info', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('open_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(default='\u5c0f\u660e', max_length=30)),
                ('sex', models.CharField(default='0', max_length=1)),
                ('phone_num', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=30, null=True)),
                ('picture', models.URLField(blank=True, null=True)),
                ('bonus_range', models.IntegerField(default=0)),
                ('snd_bonus_num', models.IntegerField(default=0)),
                ('rcv_bonus_num', models.IntegerField(default=0)),
                ('snd_bonus_value', models.IntegerField(default=0)),
                ('own_bonus_value', models.IntegerField(default=0)),
                ('own_bonus_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('own_ticket_value', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('subscribe', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiningSession',
            fields=[
                ('id_session', models.IntegerField(primary_key=True, serialize=False)),
                ('person_num', models.IntegerField(default=0)),
                ('begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('over_time', models.DateTimeField(blank=True, null=True)),
                ('total_money', models.FloatField(default=0.0)),
                ('total_bonus', models.IntegerField(default=0)),
                ('total_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DiningTable',
            fields=[
                ('index_table', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('seats', models.IntegerField(default=4)),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RcvBonus',
            fields=[
                ('id_bonus', models.IntegerField(primary_key=True, serialize=False)),
                ('bonus_type', models.IntegerField(default=0)),
                ('is_message', models.BooleanField(default=False)),
                ('message', models.CharField(blank=True, max_length=40, null=True)),
                ('is_receive', models.BooleanField(default=False)),
                ('is_refuse', models.BooleanField(default=False)),
                ('content', models.CharField(blank=True, max_length=100, null=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('number', models.IntegerField(default=0)),
                ('total_money', models.FloatField(default=0)),
                ('is_best', models.BooleanField(default=False)),
                ('consumer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='Recharge',
            fields=[
                ('id_recharge', models.IntegerField(primary_key=True, serialize=False)),
                ('recharge_value', models.FloatField(default=0.0)),
                ('recharge_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('recharge_type', models.IntegerField(default=0)),
                ('recharge_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='RecordRcvBonus',
            fields=[
                ('id_record', models.IntegerField(primary_key=True, serialize=False)),
                ('bonus_num', models.IntegerField(default=0)),
                ('record_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='SndBonus',
            fields=[
                ('id_bonus', models.IntegerField(primary_key=True, serialize=False)),
                ('bonus_type', models.IntegerField(default=0)),
                ('to_table', models.CharField(blank=True, max_length=3, null=True)),
                ('to_message', models.CharField(blank=True, max_length=140, null=True)),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('content', models.CharField(blank=True, max_length=100, null=True)),
                ('bonus_num', models.IntegerField(default=0)),
                ('number', models.IntegerField(default=0)),
                ('total_money', models.FloatField(default=0)),
                ('bonus_remain', models.IntegerField(default=0)),
                ('is_exhausted', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.DiningSession')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id_ticket', models.IntegerField(primary_key=True, serialize=False)),
                ('ticket_value', models.FloatField(default=0.0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_time', models.DateTimeField(blank=True, null=True)),
                ('consumer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualMoney',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(default='\u4e32\u4e32', max_length=40)),
                ('price', models.FloatField(default=5.0)),
                ('unit', models.CharField(default='\u4e32', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WalletMoney',
            fields=[
                ('id_money', models.IntegerField(primary_key=True, serialize=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_used', models.BooleanField(default=False)),
                ('is_send', models.BooleanField(default=False)),
                ('is_receive', models.BooleanField(default=False)),
                ('consumer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weixin.Consumer')),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.VirtualMoney')),
                ('rcv_bonus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weixin.RcvBonus')),
                ('recharge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Recharge')),
                ('snd_bonus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weixin.SndBonus')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weixin.Ticket')),
            ],
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='record_rcv_bonus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weixin.RecordRcvBonus'),
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weixin.DiningSession'),
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='snd_bonus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.SndBonus'),
        ),
        migrations.AddField(
            model_name='diningsession',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.DiningTable'),
        ),
        migrations.AddField(
            model_name='consumer',
            name='on_table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weixin.DiningTable'),
        ),
        migrations.AddField(
            model_name='consumer',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weixin.DiningSession'),
        ),
    ]
