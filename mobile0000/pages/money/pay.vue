<template>
	<view class="app">
		<view class="price-box">
			<text>支付金额</text>
			<text class="price">{{amount}}</text>
		</view>

		<view class="pay-type-list">

			<view class="type-item b-b" @click="changePayType(1)">
				<text class="icon yticon icon-weixinzhifu"></text>
				<view class="con">
					<text class="tit">微信支付</text>
					<text>推荐使用微信支付</text>
				</view>
				<label class="radio">
					<radio value="" color="#fa436a" :checked='payType == 1' />
					</radio>
				</label>
			</view>
			<view class="type-item b-b" @click="changePayType(2)">
				<text class="icon yticon icon-weixinzhifu"></text>
				<view class="con">
					<text class="tit">预付款支付</text>
					<text>加盟用户用此方法更方便哦</text>
				</view>
				<label class="radio">
					<radio value="" color="#fa436a" :checked='payType == 1' />
					</radio>
				</label>
			</view>

		</view>
		<!--<text class="mix-btn" @click="confirm">确认支付</text>-->
		<text class="mix-btn" @click="confirm()">确认支付</text>




	</view>
</template>

<script>
	export default {
		data() {
			return {
				payType: 1,
				amount: 0,
				user_id: 0,
				serial: ""


			};
		},

		async onLoad(options) {

			//这里是直接在购物车或者产品页面下单时候直接支付
			if (options.source == 1) {
				let amount = options.amount;
				this.amount = amount;
				let serial = options.serial;
				this.serial = serial;
				this.user_id = uni.getStorageSync("userDetails").id;

			}
			//这里是在查询订单页面 之后点击去付款时候 随后支付
			if (options.source == 2) {
				let data = decodeURIComponent(options.data);

				var decoded = JSON.parse(data)
				console.log(decoded)
				//在这里都改成0.01
				//let amount = decoded.info.amount;
				let amount = 0.01;
				console.log(amount)
				this.amount = amount;
				this.serial = decoded.info.serial_number;

			}

		},
		methods: {
			//选择支付方式
			changePayType(type) {
				this.payType = type;
			},

			//确认支付
			confirm: async function() {
				console.log("发起支付");
				this.loading = true;
				var serial = this.serial;
				console.log(serial)
				let that = this;

				uni.login({
					success: function(loginRes) {
						that.util.request(that.api.ApiRoot + "orders/wxpay/", {
								code: loginRes.code,
								serial: serial
							}, "POST")
							.then(function(res) {
								if (res.errno === 0) {
									console.log("统一支付接口调用成功!")
									console.log("下面是预支付信息");
									console.log(res);
   

									uni.requestPayment({
										provider: 'wxpay',
										timeStamp: res.data.timeStamp,
										nonceStr: res.data.nonceStr,
										package: 'prepay_id=' + res.data.prepay_id,
										signType: 'MD5',
										paySign: res.data.paySign,
										success: function(res) {
											console.log('success:' + JSON.stringify(res))
											uni.redirectTo({   
												url: `/pages/money/paySuccess`
											})
											return res

										},
										fail: function(res) {
											console.log('fail:' + JSON.stringify(res))
											return res;
											uni.showModal({
												content: '提示！',
												title: '支付失败'
											})
										}
									})




								} else {
									console.log('统一支付接口调用失败！')
									console.log(res)
								}
							})
					}
				})
			},
			wxpayment(data) {
				uni.requestPayment({
					provider: 'wxpay',
					timeStamp: data.timeStamp,
					nonceStr: data.nonceStr,
					package: 'prepay_id=' + data.prepay_id,
					signType: 'MD5',
					paySign: data.paySign,
					success: function(res) {
						console.log('success:' + JSON.stringify(res))
						uni.redirectTo({
							url: `/pages/money/paySuccess?amount=${this.amount}&serial=${this.serial}`
						})
						return res

					},
					fail: function(res) {
						console.log('fail:' + JSON.stringify(res))
						return res;
						uni.showModal({
							content: '提示！',
							title: '支付失败'
						})
					}
				})

			}
		}
	}
</script>

<style lang='scss'>
	.app {
		width: 100%;
	}

	.price-box {
		background-color: #fff;
		height: 265upx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		font-size: 28upx;
		color: #909399;

		.price {
			font-size: 50upx;
			color: #303133;
			margin-top: 12upx;

			&:before {
				content: '￥';
				font-size: 40upx;
			}
		}
	}

	.pay-type-list {
		margin-top: 20upx;
		background-color: #fff;
		padding-left: 60upx;

		.type-item {
			height: 120upx;
			padding: 20upx 0;
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding-right: 60upx;
			font-size: 30upx;
			position: relative;
		}

		.icon {
			width: 100upx;
			font-size: 52upx;
		}

		.icon-erjiye-yucunkuan {
			color: #fe8e2e;
		}

		.icon-weixinzhifu {
			color: #36cb59;
		}

		.icon-alipay {
			color: #01aaef;
		}

		.tit {
			font-size: $font-lg;
			color: $font-color-dark;
			margin-bottom: 4upx;
		}

		.con {
			flex: 1;
			display: flex;
			flex-direction: column;
			font-size: $font-sm;
			color: $font-color-light;
		}
	}

	.mix-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 630upx;
		height: 80upx;
		margin: 80upx auto 30upx;
		font-size: $font-lg;
		color: #fff;
		background-color: $base-color;
		border-radius: 10upx;
		box-shadow: 1px 2px 5px rgba(219, 63, 96, 0.4);
	}
</style>
