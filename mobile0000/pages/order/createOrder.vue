<template>
	<view>
		<!-- 地址 -->
		<navigator url="/pages/address/address?source=1" class="address-section">
			<view class="order-content">
				<text class="yticon icon-shouhuodizhi"></text>

				<view v-if="contact_name!=''" class="wrapper">
					<view class="u-box">
						<text class="name" v-model="name">{{contact_name}}</text>
						<text class="mobile" v-model="name">{{contact_phone}}</text>
					</view>
					<view class="address-box">
						<text class="address-area" v-model="country">{{country}} {{province}} {{city}}</text>
					</view>
					<view class="address-box">
						<text class="address-main" v-model="address">{{address}}</text>
					</view>
					<view class="address-box">
						<text class="address-postcode" v-model="postcode">邮编：{{postcode}}</text>
					</view>

				</view>
				<view v-else class="wrapper">
					<view class="address-box">
						<text class="name">请选择地址</text>
					</view>

				</view>
				<text class="yticon icon-you"></text>
			</view>
		</navigator>

		<view class="goods-section">
			<view class="g-header b-b">
				<image class="logo" src="http://duoduo.qibukj.cn/./Upload/Images/20190321/201903211727515.png"></image>
				<text class="name">开皇旗舰店</text>
			</view>
			<!-- 商品列表 -->
			<view class="cart-list">
				<block v-for="(item, index) in cartList" :key="item.id">
					<view class="g-item">
						<image :src="item.product.pic_url[1]||'/static/missing-face.png'"></image>
						<view class="right">
							<text class="title clamp">{{item.product.name}}</text>
							<view class="price-box">
								<text class="price">￥{{item.product.purchase_price}}</text>
								<text class="number">x{{item.quantity}}</text>
							</view>

						</view>
					</view>
				</block>
			</view>

		</view>
    
		<!-- 金额明细 -->
		<view class="yt-list">
			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">商品金额</text>
				<text class="cell-tip">￥{{amount}}</text>
			</view>

			<view class="yt-list-cell desc-cell">
				<text class="cell-tit clamp" v-model="amount">备注</text>
				<input class="desc" type="text" v-model="message" placeholder="请填写备注信息" placeholder-class="placeholder" />
			</view>
		</view>

		<!-- 底部 -->
		<view class="footer">
			<view class="price-content">
				<text>实付款</text>
				<text class="price-tip">￥</text>
				<text class="price">{{amount}}</text>
			</view>
			<text class="submit" @click="submit">提交订单</text>
		</view>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				user_id: 0,
				serial_number: '',
				//物品清单
				cartList: [],
				//商品总金额
				amount: 0.00,
				//商品总数量
				quantity: 0,
				contact_name: '',
				contact_phone: '',
				country: '',
				province: '',
				city: '',
				address: '',
				postcode: '',
				//备注
				message: '',

			}
		},
		onShow() {
			//获取地址 这里应该取跟用户绑定的地址

			let term = uni.getStorageSync('selected_address');
			this.contact_name = term.contact_name;
			this.contact_phone = term.contact_phone;
			this.country = term.country;
			this.province = term.province;
			this.city = term.city;
			this.address = term.address;
			this.postcode = term.postcode;
			this.serial_number = this.getSerialNumber();
		},
		onLoad(options) {
			//从商品页面传来的商品数据 source
			if (options.source == 1) {

				var product_data = JSON.parse(decodeURIComponent(options.product));
				var number = options.quantity;
				console.log(product_data)
				console.log(options.quantity)
				console.log(options.total)

				var term = {
					"product": product_data,
					"quantity": number
				}
				this.user_id = uni.getStorageSync("userDetail").id;
				this.cartList.push(term);
				this.amount = options.total;
				this.quantity = options.quantity;

				//从购物车传来source==0
			} else {
				this.cartList = JSON.parse(decodeURIComponent(options.data));
				this.amount = options.total;
				this.quantity = options.quantity;
				this.user_id = uni.getStorageSync("userDetail").id;
			}
		},
		methods: {

			//根据当前时间和随机数生成流水号
			getSerialNumber() {
				const now = new Date()
				const year = String(now.getFullYear());
				let month = String(now.getMonth() + 1);
				let day = String(now.getDate());
				let hour = String(now.getHours());
				let minutes = String(now.getMinutes());
				let seconds = String(now.getSeconds());

				month.length < 2 ? (month = "0" + month) : month;
				day.length < 2 ? (day = "0" + day) : day;
				hour.length < 2 ? (hour = "0" + hour) : hour;
				minutes.length < 2 ? (minutes = "0" + minutes) : minutes;
				seconds.length < 2 ? (seconds = "0" + seconds) : seconds;
				var yyyyMMddHHmmss = year + month + day + hour + minutes + seconds;

				return yyyyMMddHHmmss + "00001";

			},
			//提交订单
			submit() {
				var that = this
				if (!this.contact_name) {
					uni.showToast({
						title: '请选择地址',
						icon: 'none',
						duration: 2000
					});
					return false;
				}

				new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/json"
						},
						url: that.api.ApiRoot + "orders/",
						data: {
							"user": that.user_id,
							"serial_number": that.serial_number,
							"name": that.contact_name,
							"phone": that.contact_phone,
							"country": that.country,
							"province": that.province,
							"city": that.city,
							"address": that.address,
							"postcode": that.postcode,
							"message": that.message,
							"amount": that.amount,
							"quantity": that.quantity,
							"details": that.cartList

						},
						method: "POST",
						success(res) {
							if (res.statusCode == 201) {
								console.log(res)
								var amount = that.amount;
								var serial = that.serial_number;
								uni.showModal({
									title: "提示",
									content: "订单生成！",
									success: function(res) {
										if (res.confirm) {
											uni.redirectTo({
												url: `/pages/money/pay?source=1&amount=${amount}&serial=${serial}`
											})
										} else if (res.cancel) {
											uni.redirectTo({
												url: `/pages/cart/cart`
											})

										}
									}
								})

							} else {

							}

						},
						fail(res) {
							console.log(res)
							uni.showToast({
								title: '当前出现问题请稍后再试',
								icon: 'none',
								duration: 2000
							});
						}
					})
				}).catch((e) => {});





			},


			stopPrevent() {}
		}
	}
</script>

<style lang="scss">
	page {
		background: $page-color-base;
		padding-bottom: 100upx;
	}

	.address-section {
		padding: 30upx 0;
		background: #fff;
		position: relative;

		.order-content {
			display: flex;
			align-items: center;
		}

		.icon-shouhuodizhi {
			flex-shrink: 0;
			display: flex;
			align-items: center;
			justify-content: center;
			width: 90upx;
			color: #888;
			font-size: 44upx;
		}

		.cen {
			display: flex;
			flex-direction: column;
			flex: 1;
			font-size: 28upx;
			color: $font-color-dark;
		}

		.name {
			font-size: 34upx;
			margin-right: 24upx;
		}

		.address {
			margin-top: 16upx;
			margin-right: 20upx;
			color: $font-color-light;
		}

		.icon-you {
			font-size: 32upx;
			color: $font-color-light;
			margin-right: 30upx;
		}

		.a-bg {
			position: absolute;
			left: 0;
			bottom: 0;
			display: block;
			width: 100%;
			height: 5upx;
		}
	}

	.wrapper {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.address-box {
		display: flex;
		align-items: center;

		.tag {
			font-size: 24upx;
			color: $base-color;
			margin-right: 10upx;
			background: #fffafb;
			border: 1px solid #ffb4c7;
			border-radius: 4upx;
			padding: 4upx 10upx;
			line-height: 1;
		}

		.address-main {
			font-weight: bold;
			font-size: 30upx;
			color: $font-color-dark;

		}

		.address-area {
			font-size: 30upx;
			color: $font-color-dark;
		}

		.address-postcode {
			font-size: 20upx;
			color: $font-color-dark;
		}
	}

	.goods-section {
		margin-top: 16upx;
		background: #fff;
		padding-bottom: 1px;

		.g-header {
			display: flex;
			align-items: center;
			height: 84upx;
			padding: 0 30upx;
			position: relative;
		}

		.logo {
			display: block;
			width: 50upx;
			height: 50upx;
			border-radius: 100px;
		}

		.name {
			font-size: 30upx;
			color: $font-color-base;
			margin-left: 24upx;
		}

		.g-item {
			display: flex;
			margin: 20upx 30upx;

			image {
				flex-shrink: 0;
				display: block;
				width: 140upx;
				height: 140upx;
				border-radius: 4upx;
			}

			.right {
				flex: 1;
				padding-left: 24upx;
				overflow: hidden;
			}

			.title {
				font-size: 30upx;
				color: $font-color-dark;
			}

			.spec {
				font-size: 26upx;
				color: $font-color-light;
			}

			.price-box {
				display: flex;
				align-items: center;
				font-size: 32upx;
				color: $font-color-dark;
				padding-top: 10upx;

				.price {
					margin-bottom: 4upx;
				}

				.number {
					font-size: 26upx;
					color: $font-color-base;
					margin-left: 20upx;
				}
			}

			.t-price-box {
				display: flex;
				align-items: center;
				font-size: 38upx;
				color: $font-color-dark;
				padding-top: 10upx;

				.price {
					margin-bottom: 4upx;
				}


			}

			.step-box {
				position: relative;
			}
		}
	}

	.yt-list {
		margin-top: 16upx;
		background: #fff;
	}

	.yt-list-cell {
		display: flex;
		align-items: center;
		padding: 10upx 30upx 10upx 40upx;
		line-height: 70upx;
		position: relative;

		&.cell-hover {
			background: #fafafa;
		}

		&.b-b:after {
			left: 30upx;
		}

		.cell-icon {
			height: 32upx;
			width: 32upx;
			font-size: 22upx;
			color: #fff;
			text-align: center;
			line-height: 32upx;
			background: #f85e52;
			border-radius: 4upx;
			margin-right: 12upx;

			&.hb {
				background: #ffaa0e;
			}

			&.lpk {
				background: #3ab54a;
			}

		}

		.cell-more {
			align-self: center;
			font-size: 24upx;
			color: $font-color-light;
			margin-left: 8upx;
			margin-right: -10upx;
		}

		.cell-tit {
			flex: 1;
			font-size: 26upx;
			color: $font-color-light;
			margin-right: 10upx;
		}

		.cell-tip {
			font-size: 26upx;
			color: $font-color-dark;

			&.disabled {
				color: $font-color-light;
			}

			&.active {
				color: $base-color;
			}

			&.red {
				color: $base-color;
			}
		}

		&.desc-cell {
			.cell-tit {
				max-width: 90upx;
			}
		}

		.desc {
			flex: 1;
			font-size: $font-base;
			color: $font-color-dark;
		}
	}

	/* 支付列表 */
	.pay-list {
		padding-left: 40upx;
		margin-top: 16upx;
		background: #fff;

		.pay-item {
			display: flex;
			align-items: center;
			padding-right: 20upx;
			line-height: 1;
			height: 110upx;
			position: relative;
		}

		.icon-weixinzhifu {
			width: 80upx;
			font-size: 40upx;
			color: #6BCC03;
		}

		.icon-alipay {
			width: 80upx;
			font-size: 40upx;
			color: #06B4FD;
		}

		.icon-xuanzhong2 {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 60upx;
			height: 60upx;
			font-size: 40upx;
			color: $base-color;
		}

		.tit {
			font-size: 32upx;
			color: $font-color-dark;
			flex: 1;
		}
	}

	.footer {
		position: fixed;
		left: 0;
		bottom: 0;
		z-index: 995;
		display: flex;
		align-items: center;
		width: 100%;
		height: 90upx;
		justify-content: space-between;
		font-size: 30upx;
		background-color: #fff;
		z-index: 998;
		color: $font-color-base;
		box-shadow: 0 -1px 5px rgba(0, 0, 0, .1);

		.price-content {
			padding-left: 30upx;
		}

		.price-tip {
			color: $base-color;
			margin-left: 8upx;
		}

		.price {
			font-size: 36upx;
			color: $base-color;
		}

		.submit {
			display: flex;
			align-items: center;
			justify-content: center;
			width: 280upx;
			height: 100%;
			color: #fff;
			font-size: 32upx;
			background-color: $base-color;
		}
	}

	/* 购物车列表项 */
	.cart-item {
		display: flex;
		position: relative;
		padding: 30upx 40upx;

		.image-wrapper {
			width: 230upx;
			height: 230upx;
			flex-shrink: 0;
			position: relative;

			image {
				border-radius: 8upx;
			}
		}

		.checkbox {
			position: absolute;
			left: -16upx;
			top: -16upx;
			z-index: 8;
			font-size: 44upx;
			line-height: 1;
			padding: 4upx;
			color: $font-color-disabled;
			background: #fff;
			border-radius: 50px;
		}

		.item-right {
			display: flex;
			flex-direction: column;
			flex: 1;
			overflow: hidden;
			position: relative;
			padding-left: 30upx;

			.title,
			.price {
				font-size: $font-base + 2upx;
				color: $font-color-dark;
				height: 40upx;
				line-height: 40upx;
			}

			.attr {
				font-size: $font-sm + 2upx;
				color: $font-color-light;
				height: 50upx;
				line-height: 50upx;
			}

			.price {
				height: 50upx;
				line-height: 50upx;
			}
		}

		.del-btn {
			padding: 4upx 10upx;
			font-size: 34upx;
			height: 50upx;
			color: $font-color-light;
		}
	}

	/* 优惠券面板 */
	.mask {
		display: flex;
		align-items: flex-end;
		position: fixed;
		left: 0;
		top: var(--window-top);
		bottom: 0;
		width: 100%;
		background: rgba(0, 0, 0, 0);
		z-index: 9995;
		transition: .3s;

		.mask-content {
			width: 100%;
			min-height: 30vh;
			max-height: 70vh;
			background: #f3f3f3;
			transform: translateY(100%);
			transition: .3s;
			overflow-y: scroll;
		}

		&.none {
			display: none;
		}

		&.show {
			background: rgba(0, 0, 0, .4);

			.mask-content {
				transform: translateY(0);
			}
		}
	}

	/* 优惠券列表 */
	.coupon-item {
		display: flex;
		flex-direction: column;
		margin: 20upx 24upx;
		background: #fff;

		.con {
			display: flex;
			align-items: center;
			position: relative;
			height: 120upx;
			padding: 0 30upx;

			&:after {
				position: absolute;
				left: 0;
				bottom: 0;
				content: '';
				width: 100%;
				height: 0;
				border-bottom: 1px dashed #f3f3f3;
				transform: scaleY(50%);
			}
		}

		.left {
			display: flex;
			flex-direction: column;
			justify-content: center;
			flex: 1;
			overflow: hidden;
			height: 100upx;
		}

		.title {
			font-size: 32upx;
			color: $font-color-dark;
			margin-bottom: 10upx;
		}

		.time {
			font-size: 24upx;
			color: $font-color-light;
		}

		.right {
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			font-size: 26upx;
			color: $font-color-base;
			height: 100upx;
		}

		.price {
			font-size: 44upx;
			color: $base-color;

			&:before {
				content: '￥';
				font-size: 34upx;
			}
		}

		.tips {
			font-size: 24upx;
			color: $font-color-light;
			line-height: 60upx;
			padding-left: 30upx;
		}

		.circle {
			position: absolute;
			left: -6upx;
			bottom: -10upx;
			z-index: 10;
			width: 20upx;
			height: 20upx;
			background: #f3f3f3;
			border-radius: 100px;

			&.r {
				left: auto;
				right: -6upx;
			}
		}
	}
</style>
