# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 05:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='BonusMessage',
            fields=[
                ('id_message', models.IntegerField(primary_key=True, serialize=False)),
                ('message', models.CharField(blank=True, max_length=140, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('open_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('sex', models.BooleanField(default=True)),
                ('phone_num', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=30, null=True)),
                ('is_dining', models.BooleanField(default=False)),
                ('snd_bonus_num', models.IntegerField(default=0)),
                ('rcv_bonus_num', models.IntegerField(default=0)),
                ('snd_bonus_value', models.IntegerField(default=0)),
                ('own_bonus_value', models.IntegerField(default=0)),
                ('own_bonus_detail', models.CharField(blank=True, max_length=30, null=True)),
                ('own_ticket_value', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('subscribe', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_table', models.CharField(blank=True, max_length=3, null=True)),
                ('begin_time', models.DateTimeField(auto_now=True)),
                ('over_time', models.DateTimeField(blank=True, null=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='DiningTable',
            fields=[
                ('index_table', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('seats', models.IntegerField(default=0)),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PersonBonus',
            fields=[
                ('id_bonus', models.IntegerField(primary_key=True, serialize=False)),
                ('bonus_type', models.IntegerField(default=0)),
                ('to_table', models.CharField(blank=True, max_length=3, null=True)),
                ('from_table', models.CharField(blank=True, max_length=3, null=True)),
                ('to_message', models.CharField(blank=True, max_length=140, null=True)),
                ('title', models.CharField(blank=True, max_length=40, null=True)),
                ('bonus_num', models.IntegerField(default=0)),
                ('bonus_remain', models.IntegerField(default=0)),
                ('is_exhausted', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='PersonMoney',
            fields=[
                ('id_money', models.IntegerField(primary_key=True, serialize=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_used', models.BooleanField(default=False)),
                ('bonus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.PersonBonus')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='PersonRecharge',
            fields=[
                ('id_recharge', models.IntegerField(primary_key=True, serialize=False)),
                ('recharge_value', models.FloatField(default=0.0)),
                ('recharge_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('recharge_type', models.IntegerField(default=0)),
                ('recharge_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='RcvBonus',
            fields=[
                ('id_bonus', models.IntegerField(primary_key=True, serialize=False)),
                ('is_message', models.BooleanField(default=False)),
                ('is_refuse', models.BooleanField(default=False)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
                ('person_bonus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.PersonBonus')),
            ],
        ),
        migrations.CreateModel(
            name='SystemBonus',
            fields=[
                ('id_bonus', models.IntegerField(primary_key=True, serialize=False)),
                ('bonus_type', models.IntegerField(default=0)),
                ('to_message', models.CharField(blank=True, max_length=45, null=True)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('bonus_num', models.IntegerField(default=0)),
                ('bonus_remain', models.IntegerField(default=0)),
                ('is_exhausted', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin', models.ForeignKey(default=b'a', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SystemMoney',
            fields=[
                ('id_money', models.IntegerField(primary_key=True, serialize=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_used', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(default=b'a', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bonus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.SystemBonus')),
            ],
        ),
        migrations.CreateModel(
            name='SystemRecharge',
            fields=[
                ('id_recharge', models.IntegerField(primary_key=True, serialize=False)),
                ('recharge_value', models.FloatField(default=0.0)),
                ('recharge_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('recharge_person', models.CharField(default='admin', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id_ticket', models.IntegerField(primary_key=True, serialize=False)),
                ('ticket_value', models.FloatField(default=0.0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_time', models.DateTimeField(blank=True, null=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualMoney',
            fields=[
                ('name', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='systemmoney',
            name='money',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.VirtualMoney'),
        ),
        migrations.AddField(
            model_name='systemmoney',
            name='rcv_bonus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.RcvBonus'),
        ),
        migrations.AddField(
            model_name='systemmoney',
            name='recharge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.SystemRecharge'),
        ),
        migrations.AddField(
            model_name='systemmoney',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Ticket'),
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='system_bonus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.SystemBonus'),
        ),
        migrations.AddField(
            model_name='rcvbonus',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.DiningTable'),
        ),
        migrations.AddField(
            model_name='personmoney',
            name='money',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.VirtualMoney'),
        ),
        migrations.AddField(
            model_name='personmoney',
            name='rcv_bonus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.RcvBonus'),
        ),
        migrations.AddField(
            model_name='personmoney',
            name='recharge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.PersonRecharge'),
        ),
        migrations.AddField(
            model_name='personmoney',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Ticket'),
        ),
        migrations.AddField(
            model_name='consumer',
            name='on_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.DiningTable'),
        ),
        migrations.AddField(
            model_name='bonusmessage',
            name='consumer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.Consumer'),
        ),
        migrations.AddField(
            model_name='bonusmessage',
            name='rcv_bonus',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weixin.RcvBonus'),
        ),
    ]
