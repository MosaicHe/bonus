# -*- coding: utf-8 -*-
# utils.py
# Create your utils here.
import random, string
from django.core.exceptions import ObjectDoesNotExist 
from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,PersonRecharge,SystemRecharge,VirtualMoney
from .models import Dining,Ticket, PersonBonus, SystemBonus, RcvBonus, BonusMessage, SystemMoney, PersonMoney
from .admin import null_person_bonus,null_system_bonus,null_dining_table,null_consumer,null_person_recharge,null_system_recharge,null_ticket,null_rcv_bonus

import pytz
from django.utils import timezone


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


#������¼�
def action_get_bonus(openid):
	#��ϵͳ�������ѯSystemBonus����is_exhausted�ֶ�Ϊfalse�ļ�¼�����ݽ����RcvBonus���д�����¼������SystemMoney����rcv_bonus�ֶ�
	#����ͨ�������ѯPersonBonus����to_table==tableId������tableId,����DiningTable����seatsֵ�������ƽ�֣���RcvBonus���д�����¼������PersonMoney����rcv_bonus�ֶ�
	#�������������ѯPersonBonus����bonus_type==�������&&is_exhausted==False�ļ�¼�����ݽ����RcvBonus���д�����¼������PersonMoney����rcv_bonus�ֶ�
	#���������ĺ������
	'''bonus_num = 0	#ͳ�������ĺ������
	consumer = Consumer.objects.get(open_id=openid)
	sys_bonus = SystemBonus.objects.filter(is_exhausted=false)
	if len(sys_bonus):
		for bonus in sys_bonus:
			rcv_bonus = RcvBonus.objects.filter(consumer=consumer,system_bonus=bonus)
			if len(rcv_bonus) == 0:
				sys_money = SystemMoney.objects.filter(bonus=bonus)
				get_num = random.randint(1, len(sys_money))
				key = create_primary_key()
				#rcv_bonus = RcvBonus.objects.create(id_bonus=key, person_bonus=, system_bonus=bonus, consumer=consumer, table=)
	
	for bonus in sys_bonus:
		try:
			rcv_bonus = RcvBonus.objects.get(consumer=consumer,system_bonus=bonus)
		except ObjectDoesNotExist:
			pass
	
	primary_key = create_primary_key()'''
		
	pass
	
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
	
