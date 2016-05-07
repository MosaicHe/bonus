# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required

from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from django.contrib.auth import authenticate

from  weixin.models import DiningTable,VirtualMoney, SndBonus, RcvBonus, WalletMoney, Consumer
from weixin import utils

def gen_id():
    return utils.create_primary_key()

@login_required(login_url='/manager/login/')
def index(request):
    current_user = request.user
    return render_to_response("manager/account/account.html")

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/manager/account/")

# 红包统计信息
@login_required(login_url='/manager/login/')
def bonus_info(request):
    current_user = request.user
    if(current_user.username == "admin"):
        print('admin')
        is_admin = True
    else:
        is_admin = False
    return render_to_response("manager/bonus/bonus_info.html")

def send_bonus_list(request):
    bonus_list=SndBonus.objects.filter(consumer__isnull=False)
    return render_to_response("manager/bonus/bonus_list.html", {'title':'发出的红包', 'bonus_list':bonus_list})

def recv_bonus_list(request):
    bonus_list=RcvBonus.objects.all()
    return render_to_response("manager/bonus/recv_bonus_list.html", {'bonus_list':bonus_list})

def flying_bonus_list(request):
    bonus_list=SndBonus.objects.filter(is_exhausted=False)
    return render_to_response("manager/bonus/flying_bonus_list.html", {'bonus_list':bonus_list})

def create_bonus(request):
    current_user = request.user
    good_list = VirtualMoney.objects.all()
    return render_to_response("manager/bonus/create_bonus.html", {'good_list':good_list})

@csrf_exempt
def create_bonus_action(request):
    title=request.POST.get("title")
    message=request.POST.get("message")
    counter = int(request.POST.get("counter"))
    good_list = VirtualMoney.objects.all()

    total_money=0
    total_counter=0
    for good in good_list:
        good_counter = int(request.POST.get(good.name) )
        total_counter = total_counter + good_counter
        total_money =  total_money + good_counter*good.price

    if(total_counter<counter):
        return _response_json(1, u"确认物品数量总和大于红包数!")

    if(total_money==0):
        return _response_json(1, u"红包没有内容!")
    elif(limitBonus(total_money)):
        return _response_json(1, u"红包超额了!")
    else:
        bonus=SndBonus.objects.create(id_bonus=gen_id(), bonus_type=2, to_message=message, title=title, bonus_num=counter, bonus_remain=counter)
        bonus.save()
        for good in good_list:
            good_counter = int(request.POST.get(good.name) )
            for i in range(good_counter):
                w = WalletMoney.objects.create(id_money=gen_id(), bonus=bonus, money=good)
                w.save()
        return _response_json(0, u"红包发送成功!")


def bonus_detail(request):
    bonus_type = request.GET.get('type')
    id = request.GET.get('bonus_id')
    good_list = VirtualMoney.objects.all()
    content=""
    remain_content=""
    if(bonus_type=='system' or bonus_type=='send' ):
        try:
            bonus=SndBonus.objects.get(id_bonus=id)
            for good in good_list:
                wm_list = WalletMoney.objects.filter(bonus=bonus, money=good)
                counter=0
                remain_counter=0
                for w in wm_list:
                    counter += 1
                    if not w.is_receive:
                        remain_counter += 1

                if(counter>0):
                    content=content+("%d%s%s,"%(counter,good.unit, good.name))

                if(remain_counter>0):
                    remain_content=remain_content+("%d%s%s,"%(remain_counter, good.unit, good.name))

            return render_to_response("manager/bonus/bonus_detail.html", { 'bonus':bonus, 'content':content, 'remain_content':remain_content})

        except ObjectDoesNotExist:
            return render_to_response("manager/bonus/bonus_detail.html")

    elif(bonus_type=='recv'):
        bonus=Rcvonus.objects.get(id_bonus=id)
        return render_to_response("manager/bonus/bonus_detail.html", { 'bonus':bonus, 'content':content, 'remain_content':remain_content})
    else:
        return render_to_response("manager/bonus/bonus_detail.html")

#判断发送的红包是否超额
def limitBonus(total):
    return False

def sys_bonus_list(request):
    bonus_list=SndBonus.objects.filter(bonus_type=2)
    return render_to_response("manager/bonus/sys_bonus_list.html",{"bonus_list":bonus_list} )


# 管理者信息
@login_required(login_url='/manager/login/')
def account(request):
    current_user = request.user
    if(current_user.username == "admin"):
        print('admin')
        is_admin = True
    else:
        is_admin = False

    return render_to_response("manager/account/account.html",{'current_user':current_user, 'is_admin':is_admin})

def bonus_rank_list(request):
    consumer_list = Consumer.objects.all().order_by("bonus_range").reverse()
    return render_to_response('manager/bonus/bonus_rank_list.html', {'consumer_list':consumer_list} )


def account_manage(request):
    user_list = User.objects.exclude(username="admin")
    return render_to_response("manager/account/manage_account.html", {'user_list': user_list})

def account_create(request):
    current_user = request.user
    return render_to_response("manager/account/create_account.html", {'current_user': current_user})


def _response_json(state, message):
    data = {}
    data['state'] = state
    data['message'] =  message
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def action(request):
    action = request.POST.get("action")
    if(action=="register"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            User.objects.get(username=username)
            return _response_json(1, u"用户名已存在!")
        except ObjectDoesNotExist:
            user=User.objects.create_user(username=username, password=password)
            user.is_staff = True
            user.save()
            return _response_json(0, u"新增用户%s"%(username))
    elif(action=="delete"):
        username = request.POST.get("username")
        try:
            user=User.objects.get(username=username)
            user.is_active = False
            return _response_json(0, u"删除成功!")
        except ObjectDoesNotExist:
            return _response_json(0, u"删除成功!")
    elif(action=="modify_password"):
        username = request.POST.get("username")
        if(request.user.username != "admin"):
            username = request.user.username
            password = request.POST.get("password")
            if password is None:
                return _response_json(1, u"密码不正确!")
            user = authenticate(username=username, password=password)
            if user is None:
                return _response_json(1, u"密码不正确!")

        new_password = request.POST.get("new_password")
        u = User.objects.get(username=username)
        u.set_password(new_password)
        u.save()
        return _response_json(0, u"修改密码成功!")
    else:
        return _response_json(1, u"错误操作")

def change_password(request):
    current_user = request.user
    return render_to_response("manager/account/change_password.html", {'current_user': current_user})


def set_coupon_limit(request):
    current_user = request.user
    return render_to_response("manager/account/set_coupon_limit.html")


def set_bonus_limit(request):
    current_user = request.user
    return render_to_response("manager/account/set_bonus_limit.html")

#就餐信息
@login_required(login_url='/manager/login/')
def dining(request):
    current_user = request.user
    return render_to_response("manager/dining/dining.html", {'current_user':current_user})

def dining_list(request):
    current_user = request.user
    return render_to_response("manager/dining/dining_list.html")

#店内基本信息
def basic(request):
    return render_to_response("manager/basic/index.html")

def delete_account(request):
    current_user = request.user
    return render_to_response("manager/basic/delete.html")

def create_coupon(request):
    current_user = request.user
    return render_to_response("manager/basic/create_coupon.html")

def goods_info(reqeust):
    good_list = VirtualMoney.objects.all()
    return render_to_response("manager/basic/goods_info.html", {"good_list":good_list})

def good_item_edit(request):
    id = request.GET.get("good_id")
    if(id):
        action="edit"
        try:
            good = VirtualMoney.objects.get(id=id)
        except ObjectDoesNotExist:
            good=None
            action="add"
    else:
        good = None
        action="add"

    return render_to_response("manager/basic/add_edit_good.html", {'action':action, 'good':good} )

@csrf_exempt
def good_action(request):
    action = request.POST.get("action")
    if(action=='add'):
        name = request.POST.get('good_name')
        price = request.POST.get('good_price')
        unit = request.POST.get('good_unit')
        try:
            good = VirtualMoney.objects.get(name=name)
            return _response_json(1, u"已有相同名字类别!")
        except ObjectDoesNotExist:
            id = gen_id()
            good = VirtualMoney.objects.create(id=id, name=name, price=price, unit=unit)
            good.save()
            return _response_json(0, u"添加成功!")

    elif(action=='edit'):
        id = request.POST.get('good_id')
        name = request.POST.get('good_name')
        price = request.POST.get('good_price')
        unit = request.POST.get('good_unit')
        try:
            VirtualMoney.objects.filter(id=id).update( name=name, price=price, unit=unit )
            return _response_json(0, u"修改成功!")
        except ObjectDoesNotExist:
            return _response_json(1, u"不存在的数据！")

    elif(action=='delete'):
        id = request.POST.get('good_id')
        print(id)
        VirtualMoney.objects.filter(id=id).delete()
        return _response_json(0, u"删除成功!")
    else:
        return _response_json(1, u"错误操作!")

def tables_info(request):
    table_list = DiningTable.objects.all()
    return render_to_response("manager/basic/tables_info.html", {'table_list':table_list})

def table_item_edit(request):
    action="add"
    index = request.GET.get("index_table")
    if(index):
        try:
            action="edit"
            table = DiningTable.objects.get(index_table=index)
        except ObjectDoesNotExist:
            table = None
            action="add"
    else:
        action="add"
        table = None
    return render_to_response("manager/basic/add_edit_table.html", {'action':action, 'table':table})

@csrf_exempt
def table_action(request):
    #print(request.body)
    action = request.POST.get("action")
    if(action=='add'):
        index = request.POST.get("table_num")
        cap = request.POST.get("capacity")
        if(request.POST.get("is_vip")=='1'):
            is_vip = True
        else:
            is_vip = False

        try:
            DiningTable.objects.get(index_table=index)
            return _response_json(1, u"桌号已存在!")
        except ObjectDoesNotExist:
            table=DiningTable.objects.create(index_table=index, seats=int(cap), is_private=is_vip )
            table.save()
            return _response_json(0, u"增加成功!")
    elif(action=="delete"):
        index = request.POST.get("table_num")
        DiningTable.objects.filter(index_table=index).delete()
        return _response_json(0, u"删除成功!")
    elif(action=="edit"):
        index = request.POST.get("table_num")
        cap = request.POST.get("capacity")
        if(request.POST.get("is_vip")=='1'):
            is_vip = True
        else:
            is_vip = False
        DiningTable.objects.filter(index_table=index).update(seats=cap, is_private=is_vip)
        return _response_json(0, u"编辑成功!")
    else:
        return _response_json(1, u"错误操作!")


