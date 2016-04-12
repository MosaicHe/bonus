# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# �����ͳ�Ʊ�
class BonusCountDay(models.Model):
	consumer = models.CharField(primary_key=True, max_length=30)	#�û�Ψһid
	count_num = models.IntegerField(default=0)						#������ͳ����
	other_info = models.CharField(max_length=30)					#������Ʒͳ�������ַ�����ʽ


# �����ͳ�Ʊ�
class BonusCountMonth(models.Model):
	consumer = models.CharField(primary_key=True, max_length=30)	#�û�Ψһid
	count_num = models.IntegerField(default=0)						#������ͳ����
	other_info = models.CharField(max_length=30)					#������Ʒͳ�������ַ�����ʽ
	
	
#��̨��ά����̨״̬		
class DiningTable(models.Model):
	index_table = models.IntegerField(primary_key=True)	#��̨���
	status = models.BooleanField(default=False)			#��̨״̬
	seats = models.IntegerField(default=0)					#��̨��������
	is_private = models.BooleanField(default=False)		#�Ƿ��ǰ���

	def __unicode__(self):
		return "table %d"%(self.indexTable)

#���������ݱ�		
class Consumer(models.Model):
	open_id = models.CharField(max_length=30, primary_key=True)	#΢��openId
	name = models.CharField(max_length=30)							#�û���
	sex = models.BooleanField(default=True)						#�Ա�
	phone_num = models.CharField(max_length=20)					
	address = models.CharField(max_length=30)
	is_dining = models.BooleanField(default=False)					#�Ƿ��ھͲ�״̬
	snd_bonus_num = models.IntegerField(default=0)					#���������
	rcv_bonus_num = models.IntegerField(default=0)					#�պ������
	snd_bonus_value = models.IntegerField(default=0)				#��������
	own_bonus_value = models.IntegerField(default=0)				#���ú�����
	own_ticket_value = models.IntegerField(default=0)				#������ȯ���
	create_time = models.DateTimeField()							#�״ι�עʱ��
	subscribe = models.BooleanField(default=True)					#�Ƿ��ע
	on_table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)	#�Ͳ���̨
	
	def __unicode__(self):
		return self.name
		
#���˳�ֵ
class PersonRecharge(models.Model):
	id_recharge = models.IntegerField(primary_key=True)		#��ֵ��¼id
	recharge_value = models.FloatField(default=0.0)			#��ֵ���
	recharge_time = models.DateTimeField()						#��ֵʱ��
	recharge_person = models.CharField(max_length=30)			#��ֵ��
	recharge_type = models.IntegerField(default=0)				#��ֵ��ʽ��΢��/�򵥽���/���
	
	def __unicode__(self):
		return self.recharge_person
		
#ϵͳ��ֵ��¼
class SystemRecharge(models.Model):
	id_recharge = models.IntegerField(primary_key=True)		#��ֵ��¼id
	recharge_value = models.FloatField(default=0.0)			#��ֵ���
	recharge_time = models.DateTimeField()						#��ֵʱ��
	recharge_person = models.CharField(max_length=30)			#��ֵ��
	
	def __unicode__(self):
		return self.recharge_person

#�Ͳͼ�¼��		
class Dining(models.Model):
	id_dining = models.IntegerField(primary_key=True)
	id_table = models.IntegerField()		#����
	begin_time = models.DateTimeField() 	#��ʼ�Ͳ�ʱ��
	over_time = models.DateTimeField()		#�����Ͳ�ʱ��
	consumer = models.OneToOneField(Consumer, on_delete=models.CASCADE)	#����������
	
	def __unicode__(self):
		return "Dining Record %s"%(self.consumer.name)
		
		
#����ȯ
class Ticket(models.Model):
	id_ticket = models.IntegerField(primary_key=True)		#����ȯΨһid
	ticket_value = models.FloatField(default=0.0)			#ȯֵ
	create_time = models.DateTimeField()					#����ȯ����ʱ��
	valid_time = models.DateTimeField()					#����ȯ��Чʱ��
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)	#����ȯӵ����
	
#���˵ĺ��
class PersonBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)		#���˺��Ψһid
	bonus_type = models.IntegerField(default=0)			#������ͣ���ͨ���/�������/ϵͳ���
	to_table = models.IntegerField()						#�պ������̨
	from_table = models.IntegerField()						#���������̨
	to_message = models.CharField(max_length=140)			#����
	title = models.CharField(max_length=40)				#����
	create_time = models.DateTimeField()					#����ʱ��
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)	#���ͺ����
	
	def __unicode__(self):
		return self.consume.name
		
#ϵͳ�����
class SystemBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)		#ϵͳ���Ψһid
	bonus_type = models.IntegerField(default=0)			#������ͣ���ͨ���/�������/ϵͳ���
	to_message = models.CharField(max_length=45)			#����
	title = models.CharField(max_length=20)				#����
	create_time = models.DateTimeField()					#����ʱ��
	admin = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL[0])	#���ͺ����

	def __unicode__(self):
		return "System Bonus"
		
#���յĺ��
class RcvBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)						#�յ��ĺ��Ψһid
	person_bonus = models.ForeignKey(PersonBonus, on_delete=models.CASCADE)#���˺����Ψһid
	system_bonus = models.ForeignKey(SystemBonus, on_delete=models.CASCADE)#ϵͳ�����Ψһid
	table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)		#��̨��
	
	
#�������
class BonusMessage(models.Model):
	id_message = models.IntegerField(primary_key=True)						#�������Ψһid
	message = models.CharField(max_length=140)								#��������
	rcv_bonus = models.ForeignKey(RcvBonus, on_delete=models.CASCADE)		#���յĺ��Ψһid
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)		#������Ψһid
		
#ϵͳ����Ǯ��
class SystemMoney(models.Model):
	id_money = models.IntegerField(primary_key=True)				#����Ǯ�ҵ�Ψһid
	money_name = models.CharField(max_length=40)					#����Ǯ�ҵ�����
	money_value = models.FloatField(default=0.0)					#����Ǯ�ҵ���ֵ
	create_time = models.DateTimeField()							#����ʱ��
	valid_time = models.DateTimeField()							#��Чʱ��
	is_valid = models.BooleanField(default=True)					#�Ƿ���Ч
	is_used = models.BooleanField(default=False)					#�Ƿ�����
	admin = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL[0])	#Ǯ��ӵ����
	bonus = models.ForeignKey(SystemBonus, on_delete=models.CASCADE)		#���Ψһid
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)			#����ȯΨһid
	recharge = models.ForeignKey(SystemRecharge, on_delete=models.CASCADE)	#��ֵ��¼id
	
#��������Ǯ��
class PersonMoney(models.Model):
	id_money = models.IntegerField(primary_key=True)				#����Ǯ�ҵ�Ψһid
	money_name = models.CharField(max_length=40)					#����Ǯ�ҵ�����
	money_value = models.FloatField(default=0.0)					#����Ǯ�ҵ���ֵ
	create_time = models.DateTimeField()							#����ʱ��
	valid_time = models.DateTimeField()							#��Чʱ��
	is_valid = models.BooleanField(default=True)					#�Ƿ���Ч
	is_used = models.BooleanField(default=False)					#�Ƿ�����
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)		#Ǯ��ӵ����
	bonus = models.ForeignKey(PersonBonus, on_delete=models.CASCADE)		#���Ψһid
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)			#����ȯΨһid
	recharge = models.ForeignKey(PersonRecharge, on_delete=models.CASCADE)	#��ֵ��¼id
	


