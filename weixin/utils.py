# -*- coding: utf-8 -*-
# utils.py
# Create your utils here.
import random, string
from django.core.exceptions import ObjectDoesNotExist 
from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,PersonRecharge,SystemRecharge,VirtualMoney, WalletMoney
from .models import Dining,Ticket, PersonBonus, SystemBonus, RcvBonus, BonusMessage, SystemMoney, PersonMoney,SndBonus,Recharge

import pytz
from django.utils import timezone

global null_person_bonus
global null_system_bonus
global null_dining_table
global null_consumer
global admin_consumer
global null_person_recharge
global null_system_recharge
global null_recharge
global null_ticket
global null_rcv_bonus
global null_snd_bonus


COMMON_BONUS = 0	#��ͨ���
RANDOM_BONUS = 1	#�������
SYS_BONUS	= 2		#ϵͳ���

null_person_bonus = 1
null_system_bonus = 1
null_dining_table = 1
null_consumer = 1
admin_consumer = 1
null_person_recharge = 1
null_system_recharge = 1
null_ticket = 1
null_rcv_bonus = 1
null_snd_bonus = 1
null_recharge = 1 


table = DiningTable.objects.get_or_create(index_table='0')
null_dining_table=table[0]

consumer = Consumer.objects.get_or_create(open_id='2000000000', name='null', on_table=null_dining_table)
null_consumer=consumer[0]

consumer = Consumer.objects.get_or_create(open_id='3000000000', name='admin', on_table=null_dining_table)
admin_consumer=consumer[0]

person_recharge = PersonRecharge.objects.get_or_create(id_recharge=2000000000, recharge_person=null_consumer)
null_person_recharge=person_recharge[0]

system_recharge = SystemRecharge.objects.get_or_create(id_recharge=2000000000)
null_system_recharge=system_recharge[0]

recharge = Recharge.objects.get_or_create(id_recharge=2000000000, recharge_person=null_consumer)
null_recharge=system_recharge[0]

ticket = Ticket.objects.get_or_create(id_ticket=2000000000, consumer=null_consumer)
null_ticket=ticket[0]

person_bonus = PersonBonus.objects.get_or_create(id_bonus=2000000000, consumer=null_consumer)
null_person_bonus=person_bonus[0]

system_bonus = SystemBonus.objects.get_or_create(id_bonus=2000000000)
null_system_bonus=system_bonus[0]

snd_bonus = SndBonus.objects.get_or_create(id_bonus=2000000000, consumer=null_consumer, is_exhausted=True)
null_snd_bonus=snd_bonus[0]

rcv_bonus = RcvBonus.objects.get_or_create(id_bonus=2000000000, snd_bonus=null_snd_bonus, consumer=null_consumer, table=null_dining_table)
null_rcv_bonus=rcv_bonus[0]


#����û��Ƿ��ھͲ�״̬
def is_consumer_dining(openid):
	consumer = Consumer.objects.get(open_id=openid)
	return consumer.on_table.status
	
	
#�������ɷ���
def create_primary_key(key='1', length=9):
    a = list(string.digits)
    random.shuffle(a)   
    primary = key + ''.join(a[:length])
    return string.atoi(primary, 10)

#�������
def action_bonus_message(request):
	#��request�н�����openid,rcv_bonus_id,message
	#��BonusMessage���д���һ����¼
	#�޸�RcvBonus����is_message==True
	pass
	
#������
def action_bonus_refuse(request):
	#��request�н�����openid,rcv_bonus_id
	#����rcv_bonus_id�ڱ�PersonMoney���ҵ���ܵ�id_money��
	#��PersonRecharge���д���һ����¼
	pass

#΢��֧��
def action_weixin_pay(request):
	#֧���ɹ�����PersonRecharge���д���һ���¼�¼
	#��PersonMoney���д�����Ӧ�ļ�¼
	#֧��ʧ�ܣ���PersonBonus��ɾ��һ��openid�����µļ�¼
	pass
	
#��������ȯ�¼�
def action_create_ticket(request):
	#��request�н�����openid
	#��Ticket���д���һ���µļ�¼
	#����SystemMoney����ticket�ֶ�
	#����PersonMoney����ticket�ֶ�
	pass
	
#��ȡϵͳ���
def get_system_bonus():
	pass
	
#������¼�
def action_get_bonus(openid):
	#���������ĺ������
	bonus_num = 0	#ͳ�������ĺ������
	consumer = Consumer.objects.get(open_id=openid)
	snd_bonus = SndBonus.objects.filter(is_exhausted=False)
	if len(snd_bonus):
		for bonus in snd_bonus:
			rcv_bonus = RcvBonus.objects.filter(consumer=consumer,snd_bonus=bonus)
			if len(rcv_bonus) == 0:
				if (bonus.bonus_type == COMMON_BONUS) and (bonus.to_table != consumer.on_table.index_table):
					continue
				key = create_primary_key()	
				new_rcv_bonus = RcvBonus.objects.create(id_bonus=key, snd_bonus=bonus, consumer=consumer, table=consumer.on_table)													
				money = WalletMoney.objects.filter(bonus=bonus, is_receive=False)

				print('===money:%d  remain:%d==\n'%(len(money), bonus.bonus_remain))
				if bonus.bonus_remain == 1:
					get_num = len(money)
				else:
					num = len(money) - bonus.bonus_remain + 1
					get_num = random.randint(1, num)	
				print('****get_num:%d***\n'%(get_num))
				for i in range(0, get_num):
					money[i].rcv_bonus = new_rcv_bonus
					money[i].is_receive = True
					money[i].consumer = consumer
					money[i].save()	
				'''
				if bonus.bonus_type == SYS_BONUS:
					sys_money = SystemMoney.objects.filter(bonus=bonus)
					if bonus.bonus_remain == 1:
						get_num = len(sys_money)
					else:
						get_num = random.randint(1, len(sys_money))			
					for i in range(0, get_num):
						sys_money[i].rcv_bonus=new_rcv_bonus
						sys_money[i].is_receive=True
						sys_money[i].save()
				else :
					person_money = PersonMoney.objects.filter(bonus=bonus)
					if bonus.bonus_remain == 1:
						get_num = len(person_money)
					else:
						get_num = random.randint(1, len(person_money))
					for i in range(0, get_num):
						person_money[i].rcv_bonus=new_rcv_bonus
						person_money[i].is_receive=True
						person_money[i].save()
				'''
				bonus_num +=1
				bonus.bonus_remain -= 1
				if bonus.bonus_remain == 0:
					bonus.is_exhausted = True
				bonus.save()
	return str(bonus_num)
	
#����ͨ����¼�
def action_set_common_bonus(request):
	#��PersonBonus���д���һ����¼
	#��ѯConsumer����own_bonus_detail�ֶΣ��ж��Ƿ���Ҫ΢��֧��
	#�����Ҫ΢��֧�����������Ҫ֧���Ľ�Ȼ�����΢��֧��
	pass


#����������¼�
def action_set_random_bonus(request):
	#��PersonBonus���д���һ����¼
	#��ѯConsumer����own_bonus_detail�ֶΣ��ж��Ƿ���Ҫ΢��֧��
	#�����Ҫ΢��֧�����������Ҫ֧���Ľ�Ȼ�����΢��֧��	
	pass

#��ϵͳ����¼�
def action_set_system_bonus(request):
	#��ѯsettings.AUTH_USER_MODEL����own_bonus_detail�ֶΣ��ж��Ƿ������㹻������Ǯ��
	#������㹻������Ǯ�ң�����SystemBonus���д���һ����¼��������ʾ����ϵͳ��������ꡣ
	#����SystemMoney����bonus�ֶ�ֵ
	pass
	
