
//����Ч��
//���classΪtc ��ʾ
$(".tc").click(function(){
	$("#popup").fadeIn(1500);//����IDΪpopup��DIV fadeIn()��ʾ����ʱ��
	tc_center();
});

//����ˮƽ����
$(window).resize(function(){
	tc_center();
});

function tc_center(){
	var _top=($(window).height()-$(".popup").height())/2;
	var _left=($(window).width()-$(".popup").width())/2;
	
	$(".popup").css({bottom:_bottom,left:_left});
}	

function click_get_bonus(url, openid){
	// ajax ����
	var data = '{"action":"ACTION", "openid":"OPENID", "timestamp":"TIMESTAMP"}';
	var curr_time = new Date();
	data = data.replace(/ACTION/, 'ajax_get_bonus').replace(/OPENID/,openid).replace(/TIMESTAMP/, curr_time);
	
	var xmlhttp=new XMLHttpRequest();
	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			var JSONObject = JSON.parse(xmlhttp.responseText);
			if(JSONObject.status == '0')
			{
				if(JSONObject.number == '0'){
					$("#rcv_bonus").html('<font class="f_huangse">�����ˣ����������</font>');
					$("#link1").hide();
				}
				else{
					var html = '��ϲ��������<font class="f_huangse">NUMBER</font>������';
					html = html.replace(/NUMBER/, JSONObject.number);
					$("#rcv_bonus").html(html);
					$("#link2").hide();
				}				
			}
			else
			{
				alert(JSONObject.error_msg);
			}
			
			// ���ƽ����ʽ����
			tc_center();
		}
	};
	
	xmlhttp.open("POST", url, true);
	xmlhttp.send(data);
}	
	