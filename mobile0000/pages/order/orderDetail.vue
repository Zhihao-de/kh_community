<template>
	<view>
		<button class="add-btn">{{orderData.flagsTip}}</button>
		<view class="goods-section">
			<view class="g-header b-b">
				<image class="logo" src="../../static/logo.png"></image>
				<text class="name">开皇旗舰店 </text>
			</view>

			<!-- 商品列表 -->
			<view class="cart-list">
				<block v-for="(item, index) in orderData.detail" :key="item.id" @tap="naviToProductPage">
					<view class="g-item">

						<image :src="item.product.pic_url||'/static/missing-face.png'"></image>
						<view class="right">
							<text class="title clamp">{{item.product.name}}</text>
							<view class="price-box">
								<text class="price">￥{{item.price}}</text>
								<text class="number">x{{item.quantity}}</text>
							</view>
							<view class="price-box">
								<text class="fee">￥{{item.total_price}}</text>
							</view>
						</view>
						</navi>
					</view>
				</block>
			</view>

		</view>


		<!-- 金额明细 -->
		<view class="yt-list">
			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">订单编号</text>
				<text class="cell-tip">{{orderData.info.serial_number}}</text>
			</view>
			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">商品金额</text>
				<text class="cell-tip">￥{{orderData.info.amount}}</text>
			</view>

			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">创建时间</text>
				<text class="cell-tip">{{orderData.info.created_at}}</text>
			</view>
			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">支付类型</text>
				<text class="cell-tip">{{payType}}</text>
			</view>

			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">交易单号</text>
				<text class="cell-tip">{{transaction_id}}</text>
			</view>
			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">支付时间</text>
				<text class="cell-tip">{{created_at}}</text>
			</view>


			<view class="yt-list-cell b-b">
				<text class="cell-tit clamp">备注</text>
				<text class="cell-tip">{{orderData.info.message}}</text>

			</view>
		</view>

		<view class="address-section">
			<view class="order-content">
				<text class="yticon icon-shouhuodizhi"></text>
				<view class="wrapper">
					<view class="u-box">
						<text class="name">{{orderData.info.name}}</text>
						<text class="name">{{orderData.info.phone}}</text>
					</view>
					<view class="address-box">
						<text class="address-area">{{orderData.info.country}} {{orderData.info.province}} {{orderData.info.city}}
						</text>
					</view>
					<view class="address-box">
						<text class="address-main">{{orderData.info.address}}</text>
					</view>

				</view>

			</view>
		</view>
		<!--<view v-if="orderData.info.flags">
			<view v-if="flags_arr.indexOf(orderData.info.flags)!==-1" class="logistic-section">
				<logistics :wlInfo="wlInfo" :address="address"></logistics>
			</view>
		</view>-->

		<view class="page-bottom">
			<!--未付款-->
			<view v-if="orderData.info.flags===0" class="action-btn-group">
				<button type="primary" class=" action-btn no-border buy-now-btn" @click="payOrder(orderData)">立即付款</button>
				<button type="primary" class=" action-btn no-border add-cart-btn" @click="cancelOrder(orderData)">取消订单</button>
			</view>
			<!--已付款-->
			<view v-if="orderData.info.flags===1" class="action-btn-group">
				<button type="primary" class=" action-btn no-border buy-now-btn" @click='applyRefund'>申请退款</button>
				<button type="primary" class=" action-btn no-border add-cart-btn" @click="cancelOrder">取消订单</button>
			</view>
			<!--已发货-->
			<view v-if="orderData.info.flags===2" class="action-btn-group">
				<button type="primary" class=" action-btn no-border buy-now-btn" @click="confirm">确认收货</button>
				<button type="primary" class=" action-btn no-border add-cart-btn" @click="applyRefund">申请退款</button>
			</view>
			<!--订单已完成-->
			<view v-if="orderData.info.flags===3" class="action-btn-group">
				<button type="primary" disabled="true" class=" action-btn no-border buy-now-btn">订单已完成</button>
			</view>
			<!--订单已经取消-->
			<view v-if="orderData.info.flags===4" class="action-btn-group">
				<button type="primary" disabled="true" class=" action-btn no-border buy-now-btn">订单已取消</button>
			</view>
			<!--订单正在退款-->
			<view v-if="orderData.info.flags===5" class="action-btn-group">
				<button type="primary" disabled="true" class=" action-btn no-border buy-now-btn">退款进行中</button>
			</view>
			<!--订单退款已经完成-->
			<view v-if="orderData.info.flags===6" class="action-btn-group">
				<button type="primary" disabled="true" class=" action-btn no-border buy-now-btn">退款已完成</button>
			</view>
		</view>


	</view>
</template>

<script>
	import logistics from '@/components/xinyu-logistics/xinyu-logistics.vue';
	export default {
		components: {
			logistics
		},
		data() {
			return {
				orderData: {},
				transactions: {},
				transaction_id: '',
				created_at: '',
				address: {},
				wlInfo: {},
				route: {},
				payType: '',
				flags_arr: [2, 3, 4, 5, 6]
			}
		},

		onLoad(options) {
			this.orderData = JSON.parse(decodeURIComponent(options.data));
			this.loadData();

		},
		methods: {
			//挂载物流与交易数据
			async loadData() {
				var trans = await this.getTransactionInfo();
				this.transactions = trans;
				if (trans.length == 0) {
					this.payType = "暂无";
					this.transaction_id = "暂无";
					this.created_at = "暂无"
				} else {
					this.payType = await this.getPayType(trans[0].payment_method);
					console.log("支付方式为:" + trans[0].payment_method)
					this.transaction_id = trans[0].transaction_id;
					this.created_at = trans[0].created_at;
				}
				//重新修改地址格式
				this.address = {
					"country": this.orderData.info.country,
					"province": this.orderData.info.province,
					"city": this.orderData.info.city,
					"address": this.orderData.info.address
				}
				//获取物流订单号
				var myroute = await this.getOrderRoute();
				console.log(myroute)
				this.route = myroute[0];
				//查询物流详情
				//var logisticsData = await this.getlogisticInfo(myroute[0].receipt_no);
				//this.wlInfo = logisticsData;
			},
			setClipboard(str) {
				uni.setClipboardData({
					data: str,
					success: function() {
						uni.showToast({
							title: '复制成功',
							duration: 2000
						});
					}
				});
			},
			getPayType(type) {
				if (type == '0') {
					this.payType = '支付宝';

				} else if (type == '1') {
					this.payType = '微信支付';

				} else if (type == '2') {
					this.payType = '余额支付';

				} else if (type == '3') {
					this.payType = '其他';
				}

			},

			//导向商品页面
			naviToProductPage(item) {
				let id = item.product.id;
				uni.navigateTo({
					url: '/page/product/product?id=${id}'

				})
			},
			getOrderDetail(id) {
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "orders/" + this.orderData.info.id + "/details/",
						data: {
							user_id: 1
						},
						method: "GET",
						success(res) {
							resolve(res.data)
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});
			},
			getOrderRoute() {
				return new Promise(resolve => {
					uni.request({
						url: this.api.ApiRoot + "orders/" + this.orderData.info.id + "/routes/",
						method: "GET",
						success(res) {
							resolve(res.data)
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});
			},
			getlogisticInfo(id) {
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "orders/logistic/?number=" + id + "&type=auto",

						method: "GET",
						success(res) {
							resolve(res.data.result)
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});
			},
			getTransactionInfo() {
				return new Promise(resolve => {
					uni.request({
						url: this.api.ApiRoot + "orders/" + this.orderData.info.id + "/transactions/",
						method: "GET",
						success(res) {
							resolve(res.data)
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});

			},
			payOrder(item) {
				let amount = item.info.amount;
				let serial = item.info.serial_number;

				uni.redirectTo({
					url: `/pages/money/pay?source=1&amount=${amount}&serial=${serial}`
				})
			},
			cancelOrder(item) {
				//这里要加一个弹出界面提示一下
				uni.showModal({
					title: "提示",
					content: "是否要取消订单？",
					success: function(res) {
						return new Promise(resolve => {
							uni.request({
								header: {
									"content-type": "application/json"
								},
								url: this.api.ApiRoot + "orders/" + item.info.id + "/",
								data: {

									"id": item.info.id,
									"updated_at": item.info.updated_at,
									"created_at": item.info.created_at,
									"serial_number": item.info.serial_number,
									"amount": item.info.amount,
									"quantity": item.info.quantity,
									"name": item.info.name,
									"phone": item.info.phone,
									"country": item.info.country,
									"province": item.info.province,
									"city": item.info.city,
									"address": item.info.address,
									"postcode": item.info.postcode,
									"message": item.info.message,
									"flags": 4,
									"user": item.info.user
								},
								method: "PUT",
								success(res) {
									console.log(res);
									uni.redirectTo({
										url: `/pages/order/order`
									})
								},
								fail(res) {
									console.log(res)

									uni.redirectTo({
										url: `/pages/order/order`
									})
								}
							})
						}).catch((e) => {});


					}
				})




			}


		}
	}
</script>


<style lang="scss">
	page {
		background: $page-color-base;
		padding-bottom: 100upx;
	}

	.add-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 700upx;
		height: 80upx;
		font-size: 32upx;
		color: #fff;
		background-color: $base-color;
		border-radius: 10upx;
		margin-top: 20upx;
		//box-shadow: 1px 2px 5px rgba(219, 63, 96, 0.4);
	}

	.address-section {
		padding: 15upx 0;
		background: #fff;
		position: relative;
		border-radius: 20rpx;
		margin: 30rpx 20rpx 30rpx 20rpx;

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
			font-size: 24upx;
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
			font-size: 24upx;
			color: $font-color-dark;

		}

		.address-area {
			font-size: 24upx;
			color: $font-color-dark;
		}

		.address-postcode {
			font-size: 24upx;
			color: $font-color-dark;
		}
	}

	.logistic-section {
		margin-top: 0upx;
		background: #fff;
		position: relative;

	}

	.goods-section {
		margin-top: 15upx;
		background: #fff;
		padding-bottom: 1px;
		border-radius: 20rpx;
		margin: 30rpx 20rpx 30rpx 20rpx;

		.g-header {
			display: flex;
			align-items: center;
			height: 84upx;
			padding: 0 30upx;
			position: relative;

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
				font-size: 26upx;
				color: $font-color-dark;
			}

			.spec {
				font-size: 26upx;
				color: $font-color-light;
			}

			.price-box {
				display: flex;
				align-items: center;
				color: $font-color-dark;
				padding-top: 10upx;

				.price {
					font-size: 22upx;
					margin-bottom: 4upx;
				}

				.number {
					font-size: 22upx;
					color: $font-color-base;
					margin-left: 20upx;
				}

				.fee {
					font-size: 22upx;
					font-weight: 1upx;
					color: $font-color-base;


				}
			}

			.step-box {
				position: relative;
			}
		}
	}

	/* 底部操作菜单 */
	.page-bottom {
		position: fixed;
		left: 15upx;
		bottom: 15upx;
		z-index: 109;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 720upx;
		height: 100upx;
		background: rgba(255, 255, 255, .9);
		box-shadow: 0 0 20upx 0 rgba(0, 0, 0, .5);
		border-radius: 2upx;

		.p-b-btn {
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			font-size: $font-sm;
			color: $font-color-base;
			width: 96upx;
			height: 80upx;

			.yticon {
				font-size: 40upx;
				line-height: 48upx;
				color: $font-color-light;
			}

			&.active,
			&.active .yticon {
				color: $uni-color-primary;
			}

			.icon-fenxiang2 {
				font-size: 42upx;
				transform: translateY(-2upx);
			}

			.icon-shoucang {
				font-size: 46upx;
			}


		}

		.grid-dot {

			display: flex;
			flex-direction: column;
			right: -2px;

			top: 10px;
			justify-content: center;
			align-items: center;
		}



		.action-btn-group {
			display: flex;
			height: 76upx;
			border-radius: 100px;
			overflow: hidden;
			box-shadow: 0 20upx 40upx -16upx #fa436a;
			box-shadow: 1px 2px 5px rgba(219, 63, 96, 0.4);
			background: linear-gradient(to right, #ffac30, #fa436a, #F56C6C);
			margin-left: 20upx;
			position: relative;

			&:after {
				content: '';
				position: absolute;
				top: 50%;
				right: 50%;
				transform: translateY(-50%);
				height: 28upx;
				width: 0;
				border-right: 1px solid rgba(255, 255, 255, .5);
			}

			.action-btn {
				display: flex;
				align-items: center;
				justify-content: center;
				width: 180upx;
				height: 100%;
				font-size: $font-base;
				padding: 0;
				border-radius: 0;
				background: transparent;
			}
		}
	}

	.yt-list {
		margin-top: 15upx;
		background: #fff;
		border-radius: 20rpx;
		margin: 30rpx 20rpx 30rpx 20rpx;
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
		margin-top: 15upx;
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
