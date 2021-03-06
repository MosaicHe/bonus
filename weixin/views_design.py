# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.conf import settings
import django.utils.timezone as timezone
import json
from .wechat import PostResponse, wechat, TOKEN, APPID, APPSECRET
from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus

from .utils import  action_get_bonus, is_consumer_dining, handle_ajax_request, get_user_openid, decode_bonus_detail,create_bonus_dir
from .utils import check_geted_bonus, decode_choose_pay, get_bonus_type_str

ADDRESS_IP = '127.0.0.1:8000'
#ADDRESS_IP = '120.76.122.53'

REDIRECT_SA_URL = 'http://%s/weixin/view_redirect_settle_account'%(ADDRESS_IP)
REDIRECT_UA_URL = 'http://%s/weixin/view_redirect_user_account'%(ADDRESS_IP)
REDIRECT_BS_URL = 'http://%s/weixin/view_redirect_bonus_snd'%(ADDRESS_IP)
REDIRECT_BR_URL = 'http://%s/weixin/view_redirect_bonus_rcv'%(ADDRESS_IP)
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URL&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)
AJAX_REQUEST_POST_URL = 'http://%s/weixin/view_ajax_request'%(ADDRESS_IP)
GETED_BONUS_URL = 'http://%s/weixin/view_geted_bonus/?id_record=ID_RECORD'%(ADDRESS_IP)
AGAIN_GET_BONUS_URL ='http://%s/weixin/view_again_rcv_bonus/?openid=OPENID'%(ADDRESS_IP)
CREATE_COMMON_BONUS_URL = 'http://%s/weixin/view_common_bonus/?openid=OPENID'%(ADDRESS_IP)
CREATE_RANDOM_BONUS_URL = 'http://%s/weixin/view_random_bonus/?openid=OPENID'%(ADDRESS_IP)
SELF_RCV_BONUS_URL = 'http://%s/weixin/view_self_rcv_bonus/?openid=OPENID'%(ADDRESS_IP)
SELF_SND_BONUS_URL = 'http://%s/weixin/view_self_snd_bonus/?openid=OPENID'%(ADDRESS_IP)
SELF_BONUS_LIST_URL = 'http://%s/weixin/view_self_bonus_list/?openid=OPENID'%(ADDRESS_IP)
CHOOSE_PAY_URL = 'http://%s/weixin/view_choose_pay/?openid=OPENID'%(ADDRESS_IP)
SEND_MESSAGE_URL = 'http://%s/weixin/view_choose_pay'%(ADDRESS_IP)
BONUS_REFUSE_URL = 'http://%s/weixin/view_choose_pay'%(ADDRESS_IP)


# Create your views here.

class BonusContent():
	def __init__(self, name, price, unit, number):
		self.unit = unit
		self.name = name
		self.price = price
		self.number = number

#我的钱包界面
def view_user_account(request):
	pass
	
#我的钱包界面认证
def view_redirect_user_account(request):
	#获取openid
	#根据openid查询Consumer表中own_bonus_value，own_bonus_detail，own_ticket_value，刷新页面信息		
	openid = 'koovox'
	title = '我'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL	
	consumer = Consumer.objects.get(open_id=openid)
	g1 = BonusContent('123','串', '(15元/串)')
	g2 = BonusContent('234','份', '(5元/份)')
	g3 = BonusContent('567','瓶', '(6元/瓶)')
	good_list = {"串串":g1, "甜品":g2, "可乐":g3}
	return render_to_response('user_account.html', locals())
	
#结算界面
def view_settle_account(request):	
	pass
	
#结算界面认证
def view_redirect_settle_account(request):
	#获取openid
	title = '结算'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL	
	openid = "koovox"
	consumer = Consumer.objects.get(open_id=openid)
	table_total = 100
	ajax_request_url = AJAX_REQUEST_POST_URL
	return render_to_response('close_an_account.html', locals())

#发红包界面
@csrf_exempt
def view_snd_bonus(request):
	pass
	
#抢红包界面
@csrf_exempt
def view_rcv_bonus(request):
	pass
	
#抢红包界面认证
@csrf_exempt
def view_redirect_bonus_rcv(request):
	#获取openid
	#刷新页面中openid
	title = '东启湘厨'
	body_class = 'red_q'
	static_url = settings.STATIC_URL
	openid = 'koovox'
	ajax_request_url = AJAX_REQUEST_GET_URL.replace('OPENID', openid)
	geted_bonus_url = GETED_BONUS_URL
	get_bonus_url = GET_BONUS_URL
	return render_to_response('get_bonus.html', locals())

#继续抢红包界面
@csrf_exempt
def view_again_rcv_bonus(request):
	openid = request.GET.get('openid')
	print('**view_again_rcv_bonus:%s***'%(openid))
	title = '东启湘厨'
	body_class = 'red_q'
	static_url = settings.STATIC_URL
	ajax_request_url = AJAX_REQUEST_GET_URL.replace('OPENID', openid)
	geted_bonus_url = GETED_BONUS_URL
	again_get_bonus_url = AGAIN_GET_BONUS_URL.replace('OPENID', openid)
	return render_to_response('get_bonus.html', locals())
	
#发红包界面认证
@csrf_exempt
def view_redirect_bonus_snd(request):
	#获取openid
	switch = True
	if switch:
		title = '选择红包类型'
		body_class = 'red_cen'
		static_url = settings.STATIC_URL
		openid = 'koovox'
		self_rcv_bonus_url = SELF_RCV_BONUS_URL.replace('OPENID', openid)
		self_snd_bonus_url = SELF_SND_BONUS_URL.replace('OPENID', openid)
		self_bonus_list_url = SELF_BONUS_LIST_URL.replace('OPENID', openid)
		create_common_bonus_url = CREATE_COMMON_BONUS_URL.replace('OPENID', openid)
		create_random_bonus_url = CREATE_RANDOM_BONUS_URL.replace('OPENID', openid)
		return render_to_response('bonus_type.html', locals())
	else:
		title = '提示'
		article_class = 'issue-bj stanson'
		static_url = settings.STATIC_URL
		prompt_message = '就餐用户独享抢红包！'
		return render_to_response("user_prompt.html", locals())
	
#check收到的串串
@csrf_exempt
def view_self_rcv_bonus(request):
	#获取openid
	openid = request.GET.get('openid')
	print("========view_self_rcv_bonus :%s=========\n"%(openid))	
	title = '收到的串串'
	article_class = 'issue-bj'
	static_url = settings.STATIC_URL
	picture = 'http://wx.qlogo.cn/mmopen/9T7GtDDMnzaBB0ILSKYVrq1esXAVR4VKtiaYwhxOaFb7VJpgtsrsngBZRiavDsVvMibOnSxfDsZ4zGgbN6NlxB4CTIshrGAOvQD/0'
	table = DiningTable.objects.get(index_table='1')
	consumer_tuple = Consumer.objects.get_or_create(open_id=openid, name="stephen", picture=picture, on_table=table)
	consumer = consumer_tuple[0]
	rcv_bonus = RcvBonus.objects.filter(consumer=consumer).order_by("datetime").reverse()
	return render_to_response('self_rcv_bonus.html', locals())

#check发出的串串
@csrf_exempt
def view_self_snd_bonus(request):
	#获取openid
	openid = request.GET.get('openid')
	print("========view_self_rcv_bonus :%s=========\n"%(openid))	
	title = '收到的串串'
	article_class = 'issue-bj stanson'
	static_url = settings.STATIC_URL
	consumer = Consumer.objects.get(open_id=openid)
	rcv_bonus = SndBonus.objects.filter(consumer=consumer).order_by("create_time").reverse()
	return render_to_response('self_snd_bonus.html', locals())
	
#check串串排行榜
@csrf_exempt
def view_self_bonus_list(request):
	openid = request.GET.get('openid')
	print("========view_self_bonus_list :%s=========\n"%(openid))	
	title = '收到的串串'
	article_class = 'issue-bj stanson'
	static_url = settings.STATIC_URL
	oneself = Consumer.objects.get(open_id=openid)
	consumer_list = Consumer.objects.all().order_by("bonus_range").reverse()	
	top_consumer = consumer_list[0]
	return render_to_response('self_bonus_list.html', locals())
	
#发普通红包
def view_common_bonus(request):
	#从request中解析出openid
	openid = request.GET.get('openid')
	print("========view_common_bonus :%s=========\n"%(openid))
	title = '普通红包'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL
	openid = 'koovox'	
	g1 = BonusContent('123','串', '(15元/串)')
	g2 = BonusContent('234','份', '(5元/份)')
	g3 = BonusContent('567','瓶', '(6元/瓶)')
	good_list = {"串串":g1, "甜品":g2, "可乐":g3}
	choose_pay_url = CHOOSE_PAY_URL.replace("OPENID", openid)
	return render_to_response('common_bonus.html', locals())
	
#发手气红包
def view_random_bonus(request):
	#从request中解析出openid
	openid = request.GET.get('openid')
	print("========view_random_bonus :%s=========\n"%(openid))
	title = '手气红包'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL
	openid = 'koovox'		
	g1 = BonusContent('123','串', '(15元/串)')
	g2 = BonusContent('234','份', '(5元/份)')
	g3 = BonusContent('567','瓶', '(6元/瓶)')
	good_list = {"串串":g1, "甜品":g2, "可乐":g3}
	choose_pay_url = CHOOSE_PAY_URL.replace("OPENID", openid)
	return render_to_response('random_bonus.html', locals())
	
#发系统红包
def view_system_bonus(request):
	#从request中解析出adminId
	#刷新页面中的adminId	
	pass
	
class GetedBonus():
	def __init__(self, id_bonus=None, openid=None, name=None, picture=None, message=None, datetime=None, content=None, title=None):
		self.id_bonus = id_bonus
		self.openid = openid
		self.name = name
		self.picture = picture
		self.message = message
		self.datetime = datetime
		self.content = content
		self.title = title

		
#抢到的红包界面
@csrf_exempt
def view_geted_bonus(request):
	id_record = request.GET.get('id_record')
	if id_record:
		print("===view_geted_bonus:%s===\n"%(id_record))
		title = '东启湘厨'
		body_class = 'qubaba_hsbj'
		static_url = settings.STATIC_URL
		
		bonus_dir1 = {"串串":"3串", "可乐":"2瓶", "甜品":"3个"}
		bonus_dir2 = {"串串":"6串", "可乐":"4瓶", "甜品":"7个"}
		bonus_dir3 = {"串串":"10串", "可乐":"2瓶", "甜品":"8个"}
		picture1 = 'http://wx.qlogo.cn/mmopen/9T7GtDDMnzaBB0ILSKYVrq1esXAVR4VKtiaYwhxOaFb7VJpgtsrsngBZRiavDsVvMibOnSxfDsZ4zGgbN6NlxB4CTIshrGAOvQD/0'
		picture2 = ' http://wx.qlogo.cn/mmopen/ZMdxSDafpxR1pC2gQK7tKP7L2fM35ic9dOSG2eAe1icQ3cKoHA34cbWqhHHlv6fKNzFGmiaACiaqSUvQ30jLlxO9R8GQELocGjkib/0'
		curr_time = timezone.now
		random = GetedBonus(id_bonus='1234', openid="2345", name="stephen", picture=picture1, message="恭喜发财", datetime=curr_time, content=bonus_dir1)
		system = GetedBonus(id_bonus='1454', openid="6345", name="hero", picture=picture2, message="生日快乐", datetime=curr_time, content=bonus_dir2, title=title)
		common = GetedBonus(id_bonus='1904', openid="6225", name="stephen", picture=picture1, message="对面的女孩开过来", datetime=curr_time, content=bonus_dir3)
		random_bonus = []
		common_bonus = []
		system_bonus = []
		random_bonus.append(random)
		system_bonus.append(system)
		common_bonus.append(common)
		common_bonus_url = CREATE_COMMON_BONUS_URL.replace('OPENID', id_record)
		ajax_request_url = AJAX_REQUEST_POST_URL
		print("%s %s"%(common_bonus_url,ajax_request_url))
		return render_to_response('geted_bonus.html', locals())
	else:
		return HttpResponse("Error")
	


#支付页面
@csrf_exempt	
def view_choose_pay(request):
	openid = request.GET.get('openid')
	print("+++view_choose_pay %s+++\n"%(openid))
	consumer = Consumer.objects.get(open_id=openid)
	title = '东启湘厨'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL	
	g1 = BonusContent('123','串', '(15元/串)')
	g2 = BonusContent('234','份', '(5元/份)')
	g3 = BonusContent('567','瓶', '(6元/瓶)')
	good_list = {"串串":g1, "甜品":g2, "可乐":g3}	
	total_money = 105
	enough_money = False
	return render_to_response('weixin_pay.html', locals())

#网页ajax请求
@csrf_exempt
def view_ajax_request(request):
	print('***view_ajax_request body: ****\n')
	data = json.loads(request.body)
	action = data['action']
	session = request.session
	for key, value in data.items():
		print('%s ==> %s'%(key, value))
		
	
	#实现ajax请求处理函数
	response = handle_ajax_request(action, data, session)

	return HttpResponse(response)

#微信token认证
@csrf_exempt
def view_wechat_token(request):
	pass


