<template>
	<view class="content">
		<view class='intro'><text>请说明退款原因:</text>
		</view>
		<view class="mask-content-input">
			<textarea class="textarea" v-model="refund_reason" :placeholder="placeholder" :cursor-spacing="100"
			 :show-confirm-bar="false" :focus="focus" maxlength="140"></textarea>
		</view>
		<view class="btn-group">
			<button class="mix-btn" @click="refund_request()">提交</button>
			<button class="mix-btn" @click="cancel()">取消</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				orderData: {},
				refund_reason: ''

			}
		},
		onLoad(options) {
			this.orderData = JSON.parse(decodeURIComponent(options.data));

		},
		methods: {
			refund_request() {
				this.orderData.info.refund_reason = this.refund_reason;
				this.orderData.info.refund_number = this.orderData.info.serial_number;
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/json"
						},
						url: this.api.ApiRoot + "orders/" + this.orderData.info.id + "/",
						data: this.orderData.info,
						
						/*	{
							
						"id":this.orderData.info.id,
							"updated_at": this.orderData.info.updated_at,
							"created_at": this.orderData.info.created_at,
							"serial_number": this.orderData.info.serial_number,
							"amount": this.orderData.info.amount,
							"quantity": this.orderData.info.quantity,
							"name": this.orderData.info.name,
							"phone": this.orderData.info.phone,
							"country": this.orderData.info.country,
							"province": this.orderData.info.province,
							"city": this.orderData.info.city,
							"address": this.orderData.info.address,
							"postcode": item.info.postcode,
							"message": item.info.message,
							"flags": 5,
							"user": item.info.user,
							"refund_number": item.info.serial_number,
							"refund_reason": this.refund_reason
						}*/
						method: "PUT",
						success(res) {
							console.log(res);
							uni.showModal({
								title: "提示",
								content: "退款申请已经提交！",
								success: function(res) {
									if (res.confirm) {
										uni.navi({
											url: `/page/order/order`
										})

									} /*else if (res.cancel) {
										uni.redirectTo({
											url: `/page/order/order`
										})

									}*/
								}
							})

						},
						fail(res) {
							uni.showModal({
								title: "提示",
								content: "退款申请提交失败！",
							})


						}
					})
				}).catch((e) => {});


			},
			cancel() {
				uni.navigateBack({})
			}

		}
	}
</script>

<style lang='scss'>
	page,

	.content {
		height: 100%;
		background-color: #f8f8f8;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		.mask-content-input {
			width: 718upx;
			width: 100%;
			padding: 10upx 16upx 20upx;

			.textarea {
				height: 100px;
				width: 686upx;
				width: 100%;
				padding: 16upx;
				border: 2upx solid #d5d5d6;
				border-radius: 8upx;
			}
		}
	}




	.btn-group {
		padding-top: 100upx;
	}

	.mix-btn {
		margin-top: 30upx;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 600upx;
		height: 80upx;
		font-size: $font-lg;
		color: #fff;
		background-color: $base-color;
		border-radius: 10upx;

		&.hollow {
			background: #fff;
			color: #303133;
			border: 1px solid #ccc;
		}
	}
</style>
