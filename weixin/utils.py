# -*- coding: utf-8 -*-
# utils.py
# Create your utils here.


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
def action_get_bonus(request):
	#����request��openId��tableId
	#��ϵͳ�������ѯSystemBonus����is_exhausted�ֶ�Ϊfalse�ļ�¼�����ݽ����RcvBonus���д�����¼������SystemMoney����rcv_bonus�ֶ�
	#����ͨ�������ѯPersonBonus����to_table==tableId������tableId,����DiningTable����seatsֵ�������ƽ�֣���RcvBonus���д�����¼������PersonMoney����rcv_bonus�ֶ�
	#�������������ѯPersonBonus����bonus_type==�������&&is_exhausted==False�ļ�¼�����ݽ����RcvBonus���д�����¼������PersonMoney����rcv_bonus�ֶ�
	#���������ĺ������
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
	
