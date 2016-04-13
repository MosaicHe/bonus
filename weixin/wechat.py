# -*- coding: utf-8 -*-
# wechat.py
# Create your wechat here.
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages

from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,PersonRecharge,SystemRecharge,VirtualMoney
from .models import Dining,Ticket, PersonBonus, SystemBonus, RcvBonus, BonusMessage, SystemMoney, PersonMoney
from django.core.exceptions import ObjectDoesNotExist 
import pytz
from django.utils import timezone
import re

TOKEN = 'token'
APPID = 'wxc32d7686c0827f2a'
APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URI&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)

conf = WechatConf(
    token = TOKEN,
    appid = APPID,
    appsecret = APPSECRET,
    encrypt_mode = 'normal'
)

WECHAT = WechatBasic(conf = conf)

class PostResponse():
	wechat = WECHAT
	def __init__(self, request):
		try:
			wechat.parse_data(data = request.body)
		except ParseError:
			return HttpResponseBadRequest('Invalid XML Data')
		self.id = wechat.message.id
		self.target = wechat.message.target
		self.source = wechat.message.source
		self.time = wechat.message.time
		self.type = wechat.message.type
		self.raw = wechat.message.raw
		self.message = wechat.message
	
	#��ע
	def _subscribe(self):
		# �޸�DiningTable����status/seatsֵ
		curr_time = timezone.now()
		index_table = re.findall(r'\d+',self.message.key)[0]
		table = DiningTable.objects.get(index_table=index_table)
		table.status = True
		table.seats++
		table.save()
		# ��ѯConsumer������м�¼���޸�subscribe/is_diningֵ�����û�м�¼�����ȴ�΢�Ż�ȡ�û���Ϣ��Ȼ���½�һ����¼
		try:
			consumer = Consumer.objects.get(open_id=self.source)
			if consumer.subscribe == False:
				consumer.subscribe = True
		except ObjectDoesNotExist:
			# ͨ����ҳ��Ȩ��ȡ�û���Ϣ
			consumer = Consumer.objects.create(open_id=self.source)
			consumer.create_time = curr_time
		consumer.is_dining = True
		consumer.on_table = table
		consumer.save()
		# ��Dining���д���һ����¼
		dining = Dining.objects.create(id_table=index_table, begin_time=curr_time, consumer=consumer)
		dining.save()
		# ����ѡ����Ϣ	
		return wechat.response_text(content =  u'��������%s����' %(index_table))
		
	
	#ȡ����ע
	def _unsubscribe(self):
		# ����Consumer����subscribe��ΪFalse
		consumer = Consumer.objects.get(open_id=self.source)
		consumer.subscribe = False
		consumer.save()
		return ''
	
	#ɨ��
	def _scan(self):
		# �޸�DiningTable����status/seatsֵ
		curr_time = timezone.now()
		index_table = re.findall(r'\d+',self.message.key)[0]
		table = DiningTable.objects.get(index_table=index_table)
		table.status = True
		table.seats++
		table.save()		
		# ��ѯConsumer, �޸�is_diningֵΪTrue
		consumer = Consumer.objects.get(open_id=self.source)
		consumer.is_dining = True
		consumer.on_table = table
		consumer.save()		
		# ��Dining���д���һ����¼
		dining = Dining.objects.create(id_table=index_table, begin_time=curr_time, consumer=consumer)
		dining.save()		
		# ����ѡ����Ϣ
		return wechat.response_text(content =  u'��������%s����' %(index_table))
		
		
	#�˵���ת�¼�
	def _view_jump(self):
		'''����˵���ת�¼�
		1������openid,��ѯconsumer����ȡ��ǰ�û���ownBonusValue,ownTicketValue��idTable.
		2������idtable����ѯRcvBonus����ȡ�������������к��
		'''
		pass
		
	#�Զ�����
	def auto_handle(self):
		response = wechat.response_text(content='')
		if isinstance(self.message, messages.TextMessage):
			response = wechat.response_text(content=self.message.content)
		elif isinstance(self.message, messages.EventMessage):
			if self.type == 'subscribe':
				response = self._subscribe()
			elif self.type == 'unsubscribe':
				response = self._unsubscribe()
			elif self.type == 'scan':
				response = self._scan()
			elif self.type == 'view':
				pass
		
		return HttpResponse(response, content_type='application/xml')
			
		