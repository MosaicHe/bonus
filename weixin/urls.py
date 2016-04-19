from django.conf.urls import url

from . import views_design

urlpatterns = [
	url(r'^view_redirect_bonus_rcv',views_design.view_redirect_bonus_rcv, name='view_redirect_bonus_rcv'),
	url(r'^view_geted_bonus',views_design.view_geted_bonus, name='view_geted_bonus'),
	url(r'^view_again_rcv_bonus',views_design.view_again_rcv_bonus, name='view_again_rcv_bonus'),
	url(r'^view_action_get_bonus',views_design.view_action_get_bonus, name='view_action_get_bonus'),
]
