<template>
	<view class="content">
		<view class="navbar">
			<view v-for="(item, index) in navList" :key="index" class="nav-item" :class="{current: tabCurrentIndex === index}"
			 @click="tabClick(index)">
				{{item.text}}
			</view>
		</view>

		<swiper :current="tabCurrentIndex" class="swiper-box" duration="300" @change="changeTab">
			<swiper-item class="tab-content" v-for="(tabItem,tabIndex) in navList" :key="tabIndex">
				<scroll-view class="list-scroll-content" scroll-y>
					<!-- 空白页 -->
					<empty v-if="tabItem.loaded === true && tabItem.orderList.length === 0"></empty>

					<!-- 订单列表 -->
					<view class="order-item" v-for="(item,index) in tabItem.orderList" :key="index">
						<view class="i-top b-b">
							<text class="time">{{item.info.created_at}}</text>
							<text class="flags" :style="{color: item.flagsTipColor}">{{item.flagsTip}}</text>
						</view>

						<scroll-view class="goods-box" scroll-x>
							<view v-for="(goodsItem, goodsIndex) in item.detail" :key="goodsIndex" class="goods-box-single">
								<image class="goods-img" lazy-load="true" :src="goodsItem.product.pic_url || '/static/missing-face.png'" mode="aspectFill"></image>
								<view class="right">
									<text class="title clamp">{{goodsItem.product.name}}</text>
									<text class="attr-box">{{goodsItem.price}} x {{goodsItem.quantity}}</text>
									<text class="price">{{goodsItem.total_price}}</text>
				
									
								</view>
							</view>
						</scroll-view>


						<view class="price-box">
							共
							<text class="num">{{item.info.quantity}}</text>
							件商品 总计
							<text class="price">{{item.info.actual_payment}}</text>
						</view>
						<!--<view class="price-box">
							 运费
							<text class="price">{{item.info.freight}}</text>
						</view>
						<view class="price-box">
							 实付款
							<text class="price">{{item.info.actual_payment}}</text>
						</view>-->
				

						<view class="action-box b-t" v-if=" item.info.flags==0 ">
							<button class="action-btn" @click="navToDetailPage(item)">查看详情</button>
							<button class="action-btn" @click="payOrder(item)">去付款</button>
							<button class="action-btn" @click="cancelOrder(item)">取消订单</button>
						</view>
						<view class="action-box b-t" v-if=" item.info.flags == 1">
							<button class="action-btn" @click="navToDetailPage(item)">查看详情</button>
							<button class="action-btn" @click="comfirm(item)">确认收货</button>
							<button class="action-btn" @click="refund(item)">退款</button>

						</view>

						<view class="action-box b-t" v-if="item.info.flags == 2">
							<button class="action-btn" @click="navToDetailPage(item)">查看详情</button>
							<button class="action-btn" @click="navToLogisticPage(item)">物流信息</button>
							<button class="action-btn" @click="comfirm(item)">确认收货</button>
						</view>

						<view class="action-box b-t" v-if=" item.info.flags == 3 ">
							<button class="action-btn" @click="navToDetailPage(item)">查看详情</button>
							<button class="action-btn" @click="refundrequest(item)">退款</button>
						</view>
						<view class="action-box b-t" v-if=" item.info.flags == 4 ">
							<button class="action-btn" @click="navToDetailPage(item)">查看详情</button>
						</view>
						<view class="action-box b-t" v-if=" item.info.flags == 5 ">
							<button class="action-btn" @click="navToDetailPage(item)">查看详情</button>
							<button class="action-btn" disabled="true">退款中</button>
						</view>
						<view class="action-box b-t" v-if=" item.info.flags == 6 ">
							<button class="action-btn" @click="navToDetailPage(item)">查看详情</button>
						</view>
					</view>

					<uni-load-more :status="tabItem.loadingType"></uni-load-more>

				</scroll-view>
			</swiper-item>
		</swiper>
	</view>
</template>

<script>
	import uniLoadMore from '@/components/uni-load-more/uni-load-more.vue';
	import empty from "@/components/empty";
	export default {
		components: {
			uniLoadMore,
			empty
		},
		data() {
			return {
				tabCurrentIndex: 0,
				allOrders: [],
				uid: 0,

				//0 全部 1待付款 2待收货 3完成 4取消 
				navList: [{
						flags: 8,
						page: 1,
						text: '全部',
						loadingType: 'more',
						orderList: []

					},
					{
						flags: 0,
						page: 1,
						text: '待付款',
						loadingType: 'more',
						orderList: []
					},
					{
						flags: 1,
						page: 1,
						text: '待收货',
						loadingType: 'more',
						orderList: []

					},
					{
						flags: 2,
						page: 1,
						text: '已完成',
						loadingType: 'more',
						orderList: []

					},

					{
						flags: 3,
						page: 1,
						text: '已取消',
						loadingType: 'more',
						orderList: []
					},

				],
			};
		},
		onShow() {
			this.$forceUpdate()
		},
		onLoad(options) {
			/**
			 * 修复app端点击除全部订单外的按钮进入时不加载数据的问题
			 * 替换onLoad下代码即可
			 */
			//this.tabCurrentIndex = +options.flags;
			this.tabCurrentIndex = 0;
			//#ifndef MP
			this.loadData();
			//#endif
			//#ifdef MP
			//if (options.flags === 8) {
			//	this.loadData();
			//}
			this.loadData();
			//#endif

		},

		methods: {
			//发请求获取全部的订单列表

			//按标签获取分类列表
			async loadData(source) {

				//这里是将订单挂载到tab列表下
				let index = this.tabCurrentIndex;
				let navItem = this.navList[index];
				let flags = navItem.flags;

				if (source === 'tabChange' && navItem.loaded === true) {
					//tab切换只有第一次需要加载数据
					return;
				}
				if (navItem.loadingType === 'loading') {
					//防止重复加载
					return;
				}
				navItem.loadingType = 'loading';
				//获取所有的订单列表
				var orders = await this.getOrders();
				console.log(orders);
				var order_info = orders;
			
				setTimeout(() => {
					console.log(order_info);
					let orderList = order_info.filter(item => {
						//添加不同状态下订单的表现形式
						item = Object.assign(item, this.orderflagsExp(item.info.flags));
						//演示数据所以自己进行状态筛选
						if (flags === 8) {
							//8为全部订单
							return item;
						}
						//未付款的分配
						if (flags === 0) {
							return item.info.flags === 0;
						}
						//待收货
						if (flags === 1) {
							return item.info.flags === 1 || item.info.flags === 2;
						}
						//已完成
						if (flags === 2) {
							return item.info.flags === 3;
						}
						//已取消
						if (flags === 3) {
							return item.info.flags === 4;
						}
						//将退款订单放到user页面当去

					});

					//挂载在每个navibar的orderList下
					orderList.forEach(item => {
						navItem.orderList.push(item);

					});

					//loaded新字段用于表示数据加载完毕，如果为空可以显示空白页？？？
					this.$set(navItem, 'loaded', true);

					//判断是否还有数据， 有改为 more， 没有改为noMore 
					navItem.loadingType = 'noMore';
				}, 100);
			},

			//swiper 切换
			changeTab(e) {
				this.tabCurrentIndex = e.target.current;
				this.loadData('tabChange');
			},
			//顶部tab点击
			tabClick(index) {
				this.tabCurrentIndex = index;
			},
			//取消订单
			cancelOrder(item) {
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


			},

			//删除订单
			deleteOrder(index) {
				uni.showLoading({
					title: '请稍后'
				})
				setTimeout(() => {
					this.navList[this.tabCurrentIndex].orderList.splice(index, 1);
					uni.hideLoading();
				}, 600)
			},
			//发起退款
			refund(item) {
				uni.navigateTo({
					url: `/pages/money/refund?&data=${encodeURIComponent(JSON.stringify(item))}`
				})

			},

			//确认收货
			comfirm(item) {
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
							"flags": 3,
							"user": item.info.user,
							"refund_reason": '',
							"refund_number": ''
						},
						method: "PUT",
						success(res) {
							console.log(res);
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});

			},

			//发起退款

			//从服务器请求Order的信息
			getOrders() {
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "orders/queryByUser/?user_id=" + uni.getStorageSync('userDetail').id,

						method: "GET",
						success(res) {
							resolve(res.data)
							console.log(res.data)
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});
			},
			//从服务器获取订单细节

			getOrderDetails(order_id) {
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "orders/" + order_id + "/details/",

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

			//订单状态文字和颜色
			orderflagsExp(flags) {
				let flagsTip = '',
					flagsTipColor = '#fa436a';
				switch (+flags) {
					case 0:
						flagsTip = '未付款';
						flagsTipColor = '#2944fa';

						break;
					case 1:
						flagsTip = '已付款';
						flagsTipColor = '#fa38f5';
						break;
					case 2:
						flagsTip = '已配送';
						flagsTipColor = '#e7aa11';
						break;
					case 3:
						flagsTip = '已签收';
						flagsTipColor = '#0a9219';
						break;
					case 4:
						flagsTip = '已取消';
						flagsTipColor = '#fa436a';
						break;
					case 5:
						flagsTip = '申请退款中';
						flagsTipColor = '#f140fa';
						break;
					case 6:
						flagsTip = '已退款';
						flagsTipColor = '#ad2f4b';
						break;

					case 9:
						flagsTip = '订单已关闭';
						flagsTipColor = '#909399';
						break;

						//更多自定义
				}
				return {
					flagsTip,
					flagsTipColor
				};
			},

			//导航至产品详情页面
			navToDetailPage(item) {
				//测试数据没有写id，用title代替
				let msg = item;
				uni.navigateTo({
					url: `/pages/order/orderDetail?data=${encodeURIComponent(JSON.stringify(msg))}`,

				})
			},

			//导航至物流页面
			navToLogisticPage(item) {
				//测试数据没有写id，用title代替
				let msg = item;
				uni.navigateTo({
					url: `/pages/order/orderLogistic?data=${encodeURIComponent(JSON.stringify(msg))}`,

				})
			},

			//导航至产品详情页面
			payOrder(item) {
				//测试数据没有写id，用title代替
				let amount = item.info.amount;
				let serial = item.info.serial_number;

				uni.redirectTo({
					url: `/pages/money/pay?source=1&amount=${amount}&serial=${serial}`
				})
			},
			//导航至退款界面
			refundrequest(item) {
				let msg = item;
				uni.navigateTo({
					url: `/pages/money/refund?data=${encodeURIComponent(JSON.stringify(msg))}`
				})
			}


		},
	}
</script>

<style lang="scss">
	page,
	.content {
		background: $page-color-base;
		height: 100%;
	}

	.swiper-box {
		height: calc(100% - 40px);
	}

	.list-scroll-content {
		height: 100%;
	}

	.navbar {
		display: flex;
		height: 40px;
		padding: 0 5px;
		background: #fff;
		box-shadow: 0 1px 5px rgba(0, 0, 0, .06);
		position: relative;
		z-index: 10;

		.nav-item {
			flex: 1;
			display: flex;
			justify-content: center;
			align-items: center;
			height: 100%;
			font-size: 15px;
			color: $font-color-dark;
			position: relative;

			&.current {
				color: $base-color;

				&:after {
					content: '';
					position: absolute;
					left: 50%;
					bottom: 0;
					transform: translateX(-50%);
					width: 44px;
					height: 0;
					border-bottom: 2px solid $base-color;
				}
			}
		}
	}

	.uni-swiper-item {
		height: auto;
	}

	.order-item {
		display: flex;
		flex-direction: column;
		padding-left: 30upx;
		background: #fff;
		margin-top: 16upx;
		border-radius: 20rpx;
		margin: 30rpx 20rpx 30rpx 20rpx;

		.i-top {
			display: flex;
			align-items: center;
			height: 80upx;
			padding-right: 30upx;
			font-size: $font-base;
			color: $font-color-dark;
			position: relative;

			.time {
				flex: 1;
			}

			.flags {
				color: $base-color;
			}

			.del-btn {
				padding: 10upx 0 10upx 36upx;
				font-size: $font-lg;
				color: $font-color-light;
				position: relative;

				&:after {
					content: '';
					width: 0;
					height: 30upx;
					border-left: 1px solid $border-color-dark;
					position: absolute;
					left: 20upx;
					top: 50%;
					transform: translateY(-50%);
				}
			}
		}

		/* 多条商品 */
		.goods-box {
			height: flex;
			padding: 20upx 0;
			white-space: nowrap;

			/* 单条商品 */
			.goods-box-single {
				display: flex;
				padding: 20upx 0;

				.goods-img {
					display: block;
					width: 120upx;
					height: 120upx;
				}

				.right {
					flex: 1;
					display: flex;
					flex-direction: column;
					padding: 0 30upx 0 24upx;
					overflow: hidden;

					.title {
						font-size: $font-base + 2upx;
						color: $font-color-dark;
						height: 40upx;
						line-height: 40upx;
					}

					.spec {
						font-size: $font-sm + 2upx;
						color: $font-color-light;
						padding: 10upx 12upx;

						&:before {
							content: '￥';
							font-size: $font-sm;
							margin: 0 2upx 0 8upx;
						}
					}

					.attr-box {
						font-size: $font-sm + 2upx;
						color: $font-color-light;
						padding: 10upx 12upx;
					}

					.price {
						font-size: $font-base + 2upx;
						color: $font-color-dark;

						&:before {
							content: '￥';
							font-size: $font-sm;
							margin: 0 2upx 0 8upx;
						}
					}
				}
			}

			/*	.goods-item {
				width: 120upx;
				height: 120upx;
				display: inline-block;
				margin-right: 24upx;
			}

			.goods-img {
				display: block;
				width: 100%;
				height: 100%;
			}*/
		}

		/* 单条商品 */
		.goods-box-single {
			display: flex;
			padding: 20upx 0;

			.goods-img {
				display: block;
				width: 120upx;
				height: 120upx;
			}

			.right {
				flex: 1;
				display: flex;
				flex-direction: column;
				padding: 0 30upx 0 24upx;
				overflow: hidden;

				.title {
					font-size: $font-base + 2upx;
					color: $font-color-dark;
					line-height: 1;
				}

				.attr-box {
					font-size: $font-sm + 2upx;
					color: $font-color-light;
					padding: 10upx 12upx;

					&:before {
						content: '￥';
						font-size: $font-sm;
						margin: 0 2upx 0 8upx;
					}
				}

				.price {
					font-size: $font-base + 2upx;
					color: $font-color-dark;

					&:before {
						content: '￥';
						font-size: $font-sm;
						margin: 0 2upx 0 8upx;
					}
				}
			
			}
		}

		.price-box {
			display: flex;
			justify-content: flex-end;
			align-items: baseline;
			padding: 20upx 30upx;
			font-size: $font-sm + 2upx;
			color: $font-color-light;

			.num {
				margin: 0 8upx;
				color: $font-color-dark;
			}

			.price {
				font-size: $font-lg;
				color: $font-color-dark;

				&:before {
					content: '￥';
					font-size: $font-sm;
					margin: 0 2upx 0 8upx;
				}
			}
			.weight{
				font-size: $font-lg;
				color: $font-color-dark;
				
			}
		}

		.action-box {
			display: flex;
			justify-content: flex-end;
			align-items: center;
			height: 100upx;
			position: relative;
			padding-right: 30upx;
		}

		.action-btn {
			width: 160upx;
			height: 60upx;
			margin: 0;
			margin-left: 24upx;
			padding: 0;
			text-align: center;
			line-height: 60upx;
			font-size: $font-sm + 2upx;
			color: $font-color-dark;
			background: #fff;
			border-radius: 100px;

			&:after {
				border-radius: 100px;
			}

			&.recom {
				background: #fff9f9;
				color: $base-color;

				&:after {
					border-color: #f7bcc8;
				}
			}
		}
	}


	/* load-more */
	.uni-load-more {
		display: flex;
		flex-direction: row;
		height: 80upx;
		align-items: center;
		justify-content: center
	}

	.uni-load-more__text {
		font-size: 28upx;
		color: #999
	}

	.uni-load-more__img {
		height: 24px;
		width: 24px;
		margin-right: 10px
	}

	.uni-load-more__img>view {
		position: absolute
	}

	.uni-load-more__img>view view {
		width: 6px;
		height: 2px;
		border-top-left-radius: 1px;
		border-bottom-left-radius: 1px;
		background: #999;
		position: absolute;
		opacity: .2;
		transform-origin: 50%;
		animation: load 1.56s ease infinite
	}

	.uni-load-more__img>view view:nth-child(1) {
		transform: rotate(90deg);
		top: 2px;
		left: 9px
	}

	.uni-load-more__img>view view:nth-child(2) {
		transform: rotate(180deg);
		top: 11px;
		right: 0
	}

	.uni-load-more__img>view view:nth-child(3) {
		transform: rotate(270deg);
		bottom: 2px;
		left: 9px
	}

	.uni-load-more__img>view view:nth-child(4) {
		top: 11px;
		left: 0
	}

	.load1,
	.load2,
	.load3 {
		height: 24px;
		width: 24px
	}

	.load2 {
		transform: rotate(30deg)
	}

	.load3 {
		transform: rotate(60deg)
	}

	.load1 view:nth-child(1) {
		animation-delay: 0s
	}

	.load2 view:nth-child(1) {
		animation-delay: .13s
	}

	.load3 view:nth-child(1) {
		animation-delay: .26s
	}

	.load1 view:nth-child(2) {
		animation-delay: .39s
	}

	.load2 view:nth-child(2) {
		animation-delay: .52s
	}

	.load3 view:nth-child(2) {
		animation-delay: .65s
	}

	.load1 view:nth-child(3) {
		animation-delay: .78s
	}

	.load2 view:nth-child(3) {
		animation-delay: .91s
	}

	.load3 view:nth-child(3) {
		animation-delay: 1.04s
	}

	.load1 view:nth-child(4) {
		animation-delay: 1.17s
	}

	.load2 view:nth-child(4) {
		animation-delay: 1.3s
	}

	.load3 view:nth-child(4) {
		animation-delay: 1.43s
	}

	@-webkit-keyframes load {
		0% {
			opacity: 1
		}

		100% {
			opacity: .2
		}
	}
</style>
