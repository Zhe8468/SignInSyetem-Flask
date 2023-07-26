function bindCaptchaButton() {
	$("#captcha-btn").on("click",function (event) {
		var $this = $(this);
		var email = $("input[name='email']").val();
		if(!email){
			alert("请先输入邮箱！");
			return;
		}
		//通过ajax发送请求
		$.ajax({
			method: "POST",
			//这里captcha后面的斜杆加不加取决于识图函数里面有没有加斜杠 不要乱加
			url: '/users/captcha',
			data: {
				"email": email
			},
			dataType: "json",
			success: function (res) {
				var code = res['code'];
				if(code===200) {
					alert("验证码发送成功！");
					//取消点击事件
					$this.off("click");
					//开始倒计时
					var countDown = 60;
					//设置定时器
					var timer = setInterval(function () {
						countDown-=1;
						if(countDown>0){
							$this.text(countDown+" 秒后重新发送");
						}else{
							$this.text("发送验证码");
							//重新绑定点击事件
							bindCaptchaButton();
							//不需要倒计时了，清空计时器
							clearInterval(timer);
						}
					},1000);
				}
			},
			error: function (e) {
				console.log(e);
			}
		})
	});
}
$(function () {
	bindCaptchaButton();
});