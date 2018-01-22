/**
 * jQuery.ScrollTo - Easy element scrolling using jQuery. * 
 * Dual loginFROM
 * Date: 25/1/2016
 * @author zhuxd@163.com
 * @version 1.0 *
 * http://51cto.com
 */
$(function(){ 
	function oi86ydsq(){
         var passd = $("#loginform-password").val(); 		
		if(passd.length < 1 ){	
            cssLise9sd('1',8,2);return false;
		 }else{
			 cssLise9sd('1',9,2);return false;
		 }
	}
	function kie93882(){
		if($("#loginform-username").val()==false  ){
			cssLise9sd('0',8,2);return false;			
		 }else{
			 cssLise9sd('0',9,2); return false;
		 }
        if($("#loginform-password").val().length < 1){
			cssLise9sd('1',8,2);return false;
		}else{
			cssLise9sd('1',9,2);return false;
		}		 
	}	
	$(".pass input").blur(function(){
		oi86ydsq();		 
	})	
	$(".pass input").change(function(){		
		oi86ydsq();		 
	})	
	$(".user input").change(function(){
		kie93882();
	})
	$(".user input").blur(function(){        		
		kie93882();
	})
	$('.loginbtn').click(function(){	
		if($("#loginform-username").val()==false  ){
           cssLise9sd('0',8,'账号不能为空');return false;
		}
        if($("#loginform-password").val().length < 1){
		  cssLise9sd('1',8,'密码不能为空');	return false;		  	 
	    }
		if($("#verifyys").val()==''){
			$(".verifyerror").html("验证码不能为空");return false;
		}			
     });
	function cssLise9sd(ius,sddk,oies){
		if(oies!=2){
			$(".inpBox .error_9o8Kl").eq(ius).html(oies);
		}
		if(sddk==8){		
			$(".inpBox .error_9o8Kl").eq(ius).css('display','block');
		}
		if(sddk==9){
			$(".inpBox .error_9o8Kl").eq(ius).css('display','none')
		}
	}
	function Lisyye73SAks(){
		if($(".pass .error_9o8Kl").text()==''){		   
		   cssLise9sd('1',9,2);
		}else{
		  cssLise9sd('1',8,2);
		}		
	}
	$(".code .clearfix input").blur(function(){
		$(".verifyerror").show();
		if($("#verifyys").val()==''){			
			$(".verifyerror").html("验证码不能为空")
		}else{
			$.ajax({
				type:'post',
				data:{'code':$("#verifyys").val(),'_csrf':yii.getCsrfToken()},
				datatype:'json',
				url:'/index/check-verify',
				success:function(data){
					if(data!='ok'){
						$(".verifyerror").html(data)
					}else{
						$(".verifyerror").hide();
					}
				}
			})			
		}
	})
	
	Lisyye73SAks();
})
/*设置手机发送验证码开始*/
	var wait=60; 
	function time(o) { 
		if (wait == 0) { 
		o.removeAttribute("disabled"); 
		o.value="获取验证码"; 
		wait = 60;
		} else { 
		o.setAttribute("disabled", true); 
		o.value="重新发送" + wait + "s"; 
		wait--; 
		setTimeout(function() {
		time(o) 
		}, 1000) 
		} 
	}
    $(function(){
        if($("#get_verify").length){
            document.getElementById("get_verify").onclick=function(){
                var sendtype = $("#jsSendType").val();
                var sendstr = $("#jsSendStr").val();
                sendCode(this,sendstr,sendtype);time(this);
            }
        }
    });
var mobilePatten = /(^0{0,1}1[3|4|5|6|7|8|9][0-9]{9}$)/;
var emailPatten = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
function sendCode(obj,sendstr,sendtype){
    if(sendtype ==1 && !mobilePatten.test(sendstr)){
        showMess(obj,"手机号格式不正确",'errors'); return ;
    }
	 if(sendtype == 0 && !emailPatten.test(sendstr)){
        showMess(obj,"邮箱格式不正确",'errors'); return ;
    }
   
	var url = '/index/send-code';	
    $.ajax({
        type:'post',
        data:{'send_type':sendtype,'send_str':sendstr,'_csrf':yii.getCsrfToken()},
        datatype:'json',
        url:url,
        success:function(data){
            if(data == 'ok'){
                sendtype == 1 ? $(".jsMobileInfo").show() : $(".jsEmailInfo").show();
                showMess(obj,"",'success'); return ;
            }
        }
    })
}
$(function(){
	$("#user_verify").blur(function(){
		var code = $(this).val();
		var uid = $("#jsUid").val();
        var sendtype = $("#jsSendType").val();
        var sendstr = $("#jsSendStr").val();
        var obj = $(this);
        var checkVerify = 0;
        if(code){
			  $.ajax({
					type:'post',
					data:{'send_type':sendtype,'send_str':sendstr,'_csrf':yii.getCsrfToken(),code:code,uid:uid},
					dataType:'json',
                    async:false,
					url:'/index/check-code',
					success:function(data){
						if(data == true){
                            checkVerify = 1;
                            showMess(obj,"",'success');
						}else{
                            showMess(obj,"验证码错误",'errors');
                        }
					}
			 });
		}else{
			 showMess(obj,"验证码错误",'errors');
		}
        $("#jsCheckCode").val(checkVerify);return;
	});
    $("#jsValidateCode").click(function(){
        $("#user_verify").blur();
        var checkVerify = $("#jsCheckCode").val();
        if(checkVerify == 1){
            $(".loginbtn").submit();
        }

    });
});
function showMess(obj,data,type){
    if(type=='errors'){
        $(obj).parent().next(".ts_error").empty().append("<i class ='icon_erro left'></i>"+data);
		$(obj).parent().next(".ts_error").show();
        $(obj).parent().next(".ts_correct").hide();
    }else{
        $(obj).parent().next(".ts_error").empty();
        $(obj).parent().next(".ts_correct").hide();
        $(obj).parent().next(".ts_correct").show();
    }
  
    return false;
}