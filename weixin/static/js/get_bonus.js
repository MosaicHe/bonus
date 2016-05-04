
function click_get_bonus(url, openid){
	$(".tch-share").addClass("tch-modal-active");	
	if($(".tchsharebg").length>0){
		$(".tchsharebg").addClass("tchsharebg-active");
	}else{
		$("body").append('<div class="tchsharebg"></div>');
		$(".tchsharebg").addClass("tchsharebg-active");
	}
	$(".tchsharebg-active,.tchshare_btn").click(function(){
		$(".tch-share").removeClass("tch-modal-active");	
		setTimeout(function(){
			$(".tchsharebg-active").removeClass("tchsharebg-active");	
			$(".tchsharebg").remove();	
		},300);
	});
	
	// ajax ����
	var data = '{"action":"ACTION", "openid":"OPENID", "timestamp":"TIMESTAMP"}';
	var curr_time = new Date();
	data = data.replace(/ACTION/, 'ajax_get_bonus').replace(/OPENID/,openid).replace(/TIMESTAMP/, curr_time);
	ajax_get_bonus(url, data);		
}	
	
function ajax_get_bonus(url, data)
{
	
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
			
		}
	};
	
	xmlhttp.open("POST", url, true);
	xmlhttp.send(data);
}	
	
