<template>
	<view class="container">
		<view class="carousel">
			<swiper indicator-dots circular=true duration="400">
				<swiper-item class="swiper-item" v-for="(item,index) in productObj.carousal_urls" :key="index">
					<view class="image-wrapper">
						<image :src="item" class="loaded" mode="aspectFill"></image>
					</view>
				</swiper-item>
			</swiper>
		</view>

		<view class="introduce-section">

			<view class="price-box" v-if="role==2">
				<text class="price-tip">¥</text>
				<text class="price">{{productObj.purchase_price_register}}</text>
			</view>
			<view class="price-box" v-if="role==5">
				<text class="price-tip">¥</text>
				<text class="price">{{productObj.purchase_price_corporate}}</text>
			</view>

			<view class="price-box" v-if="role==0||role==1||role==3||role ==4">
				<text class="price-tip">¥</text>
				<text class="price">{{productObj.retail_price}}</text>
			</view>



			<text class="title">{{productObj.name}}</text>

		</view>


		<!--  分享 -->
		<view class="share-section" @click="share">
			<view class="share-icon">
				<text class="yticon icon-xingxing"></text>
				积
			</view>
			<text class="tit">购买该商品可获得积分</text>
			<text class="yticon icon-bangzhu1"></text>
			<view class="share-btn">
				积分查询
				<text class="yticon icon-you"></text>
			</view>

		</view>


		<view class="c-list">
			<!--
			<view class="c-row b-b" @click="toggleSpec">
				<text class="tit">购买类型</text>
				<view class="con">
					<text class="selected-text" v-for="(sItem, sIndex) in specSelected" :key="sIndex">
						{{sItem.name}}
					</text>
				</view>
				<text class="yticon icon-you"></text>
			</view>-->
			<!--<view class="c-row b-b">
				<text class="tit">优惠券</text>
				<text class="con t-r red">领取优惠券</text>
				<text class="yticon icon-you"></text>
			</view>
			<view class="c-row b-b">
				<text class="tit">促销活动</text>
				<view class="con-list">
					<text>新人首单送20元无门槛代金券</text>
					<text>订单满50减10</text>
					<text>订单满100减30</text>
					<text>单笔购买满两件免邮费</text>
				</view>
			</view>-->

			<view class="c-row b-b">
				<text class="tit">购买数量</text>
				<view class="con">
					<view class="item-list">
						<view class="number-item">
							<view class="selnum">
								<view class="cut" @click="cutNumber">-</view>
								<input v-model="number" class="number" disabled="true" type="number" />
								<view class="add" @click="addNumber">+</view>
							</view>
						</view>
					</view>
				</view>

			</view>
			<view class="c-row b-b">
				<text class="tit">服务</text>
				<view class="bz-list con">
					<text>7天无理由退换货 ·</text>
					<text>假一赔十 ·</text>
				</view>
			</view>
			<view class="c-row b-b">
				<text class="tit">运费</text>
				<view class="bz-list con">
					<text>¥30</text>
					<text>单果</text>
				</view>
			</view>
		</view>


		<view class="detail-desc">
			<view class="d-header">
				<text>图文详情</text>
			</view>
			<rich-text :nodes="string"></rich-text>
		</view>

		<!-- 底部操作菜单 -->

		<view class="page-bottom">
			<navigator url="/pages/index/index" open-type="switchTab" class="p-b-btn">
				<text class="yticon icon-xiatubiao--copy"></text>
				<text>首页</text>
			</navigator>
			<navigator url="/pages/cart/cart" open-type="switchTab" class="p-b-btn">
				<view class="grid-dot">
					<uni-badge :text="cart.length" size="small" type="primary"></uni-badge>
				</view>
				<text class="yticon icon-gouwuche"></text>


				<text>购物车</text>
			</navigator>

			<view class="action-btn-group">
				<button v-if="role==2|| role ==5" type="primary" class=" action-btn no-border buy-now-btn" @click="goCreateOrder">
					立即购买
				</button>

				<button v-else type="primary" class=" action-btn no-border buy-now-btn" @click="goCreateIntention">
					立即下单
				</button>
				<!--
				<button type="primary" class=" action-btn no-border buy-now-btn" @click="toggle">立即购买</button>-->
				<button type="primary" class=" action-btn no-border add-cart-btn" @click="addCart">加入购物车</button>
			</view>
		</view>


	</view>

</template>

<script>
	import uniBadge from "@/components/uni-badge/uni-badge.vue";
	import popupLayer from "@/components/popup-layer/popup-layer.vue";
	export default {
		components: {
			uniBadge,
			popupLayer

		},


		data() {
			return {

				cart: [],
				productObj: {
					id: '',
					name: '榴莲',
					weight: '',
					purchase_price_corporate: 0,
					purchase_price_register: 0,
					retail_price: 0,
					flag: 1,
					name: 0,
					title: 0,
					pic_url: '',
					carousal_urls: [],
					description: "这是产品描述",
					stock: 0,
					point: 0
				},
				number: 1,
				role: 0,
			};
		},

		onShow() {},
		async onLoad(options) {
			//接收传值,id里面放的是标题，因为测试数据并没写id 
			let id = options.id;
			if (id) {

				//产品展示页面
				this.productObj.id = id;
				let res = await this.getGoodsDetail(id);
				this.productObj.name = res.name;
				this.productObj.category = res.category;
				this.productObj.retail_price = res.retail_price;
				this.productObj.purchase_price_corporate = res.purchase_price_corporate;
				this.productObj.flags = res.flags;
				this.productObj.point = res.point;
				var pic_array = res.carousal_urls.split(',');
				pic_array.forEach(item => {
					console.log(item);
					console.log("ppppppp");

				})

				this.productObj.carousal_urls = pic_array;
				this.productObj.pic_url = res.pic_url;
				this.productObj.stock = res.stock;
				this.productObj.description = res.description;
				this.productObj.created_at = res.created_at;
				//产品单品信息


			}
			this.cart = uni.getStorageSync("cart");
			this.role = uni.getStorageSync("userDetail").flags;

		},
		methods: {

			getGoodsDetail(id) {
				let that = this;
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: that.api.ApiRoot + "products/" + id + "/",
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


			//数量减一
			cutNumber: function() {
				if (this.number - 1 > 1) {
					this.number = this.number - 1;
				} else {
					this.number = 1;
				}

			},
			//数量加一
			addNumber: function() {
				this.number = this.number + 1
			},
			//判断提交条件
			submitCheck() {
				let that = this;
				if (this.productObj.stock >= this.number) {
					return true;
				} else {
					uni.showModal({
						title: '提示',
						content: "购买数量大于库存数量,请修改数量！",
						success: function(res) {}
					});
					return false;
				}
			},
			//下单
			goCreateOrder() {
				if (this.submitCheck()) {
					//注册用户下单
					if (this.role == 2) {
						let that = this;
						var total_price = this.productObj.purchase_price_register * this.number;
						var num = this.number;
						var total = Number(total_price.toFixed(2));
						var credits = this.productObj.point * this.number;
						console.log("用户获得的积分为" + credits);
					}
					//加盟用户下单ssss
					if (this.role == 5) {
						let that = this;
						var total_price = this.productObj.purchase_price_corporate * this.number;
						var num = this.number;
						var total = Number(total_price.toFixed(2));
						var credits = this.productObj.point * this.number;
						console.log("用户获得的积分为" + credits);
					}
					uni.navigateTo({
						url: `/pages/order/createOrder?source=1&total=${total}&credits=${credits}&quantity=${num}&product=${encodeURIComponent(JSON.stringify(this.productObj))}`
					})
				}

			},

			//下留言订单
			goCreateIntention() {
				if (this.submitCheck()) {
					let that = this;
					var total_price = this.productObj.retail_price * this.number;
					var total = Number(total_price.toFixed(2));
					uni.navigateTo({
						url: `/pages/order/createIntention?source=1&quantity=${this.number}&total=${total}&product=${encodeURIComponent(JSON.stringify(this.productObj))}`
					})

				}
			},

			//加入购物车
			addCart() {
				if (this.submitCheck()) {
					let that = this;
					let term = {
						product: this.productObj,
						quantity: this.number
					};
					uni.setTabBarBadge({
						index: 0,
						text: "1"
					})
					uni.showToast({
						title: "已加入购物车",
						content: "已加入购物车"
					})

					let cart_term = uni.getStorageSync('cart');

					if (cart_term.length === 0) {
						cart_term.push(term);
					} else {
						let flag = false;
						for (var i = 0; i < cart_term.length; i++) {
							if (cart_term[i].product.id == term.product.id) {
								cart_term[i].quantity = cart_term[i].quantity + term.quantity;
								flag = true;
							}
						}
						if (flag == false) {
							cart_term.push(term);
						}
					}

					uni.setStorageSync("cart", cart_term);

					uni.redirectTo({
						url: "/pages/category/category"
					})
				}
			},
			toggle() {
				this.$refs.popup.open()
			},
			change(e) {
				console.log('popup ' + e.type + ' 状态', e.show)
			},
			stopPrevent() {}
		}
	}
</script>

<style lang='scss'>
	page {
		background: $page-color-base;
		padding-bottom: 160upx;
	}

	.icon-you {
		font-size: $font-base + 2upx;
		color: #888;
	}

	.carousel {
		height: 722upx;
		position: relative;

		swiper {
			height: 100%;
		}

		.image-wrapper {
			width: 100%;
			height: 100%;
		}

		.swiper-item {
			display: flex;
			justify-content: center;
			align-content: center;
			height: 750upx;
			overflow: hidden;

			image {
				width: 100%;
				height: 100%;
			}
		}

	}

	/* 标题简介 */
	.introduce-section {
		background: #fff;
		padding: 20upx 30upx;

		.title {
			font-size: 32upx;
			color: $font-color-dark;
			height: 50upx;
			line-height: 50upx;
		}

		.price-box {
			display: flex;
			align-items: baseline;
			height: 64upx;
			padding: 10upx 0;
			font-size: 26upx;
			color: $uni-color-primary;
		}

		.price {
			font-size: $font-lg + 4upx;
		}

		.m-price {
			margin: 0 12upx;
			color: $font-color-light;
			text-decoration: line-through;
		}

		.coupon-tip {
			align-items: center;
			padding: 4upx 10upx;
			background: $uni-color-primary;
			font-size: $font-sm;
			color: #fff;
			border-radius: 6upx;
			line-height: 1;
			transform: translateY(-4upx);
		}

		.bot-row {
			display: flex;
			align-items: center;
			height: 50upx;
			font-size: $font-sm;
			color: $font-color-light;

			text {
				flex: 1;
			}
		}
	}

	.c-list {
		font-size: $font-sm + 2upx;
		color: $font-color-base;
		background: #fff;

		.c-row {
			display: flex;
			align-items: center;
			padding: 20upx 30upx;
			position: relative;
		}

		.tit {
			width: 140upx;
		}

		.con {
			flex: 1;
			color: $font-color-dark;
			text-align: right;

			.selected-text {
				margin-right: 10upx;
			}
		}

		.bz-list {
			height: 40upx;
			font-size: $font-sm+2upx;
			color: $font-color-dark;

			text {
				display: inline-block;
				margin-right: 30upx;
			}
		}

		.con-list {
			flex: 1;
			display: flex;
			flex-direction: column;
			color: $font-color-dark;
			line-height: 40upx;
		}

		.red {
			color: $uni-color-primary;
		}
	}

	.number-item {
		.add {
			width: 93.75upx;
			height: 100%;
			text-align: center;
			line-height: 65upx;
		}

		.selnum {
			width: 322upx;
			height: 71upx;
			border: 2upx solid #ccc;
			display: flex;
		}

		.cut {
			width: 93.75upx;
			height: 100%;
			text-align: center;
			line-height: 65upx;
		}

		.number {
			flex: 1;
			height: 100%;
			text-align: center;
			line-height: 68.75upx;
			border-left: 2upx solid #ccc;
			border-right: 2upx solid #ccc;
			float: left;
		}
	}

	/*  详情 */
	.detail-desc {
		background: #fff;
		margin-top: 16upx;

		.d-header {
			display: flex;
			justify-content: center;
			align-items: center;
			height: 80upx;
			font-size: $font-base + 2upx;
			color: $font-color-dark;
			position: relative;

			text {
				padding: 0 20upx;
				background: #fff;
				position: relative;
				z-index: 1;
			}

			&:after {
				position: absolute;
				left: 50%;
				top: 50%;
				transform: translateX(-50%);
				width: 300upx;
				height: 0;
				content: '';
				border-bottom: 1px solid #ccc;
			}
		}
	}

	/*底部弹出框*/
	.popup-content {
		background-color: #fff;
		padding: 15px;

		.title {
			font-size: $font-base - 4upx;
			color: $font-color-dark;
			height: 40upx;
			line-height: 40upx;
		}


		.a-t {
			display: flex;

			image {
				width: 170upx;
				height: 170upx;
				flex-shrink: 0;
				margin-top: -40upx;
				border-radius: 8upx;
				;
			}

			.right {
				display: flex;
				flex-direction: column;
				padding-left: 24upx;
				font-size: $font-sm + 2upx;
				color: $font-color-base;
				line-height: 42upx;

				.price {
					font-size: $font-lg;
					color: $uni-color-primary;
					margin-bottom: 10upx;
				}

				.selected-text {
					margin-right: 10upx;
				}
			}
		}

		.attr-list {
			display: flex;
			flex-direction: column;
			font-size: $font-base + 2upx;
			color: $font-color-base;
			padding-top: 30upx;
			padding-left: 10upx;
		}

		.item-list {
			padding: 20upx 0 0;
			display: flex;
			flex-wrap: wrap;

			text {
				display: flex;
				align-items: center;
				justify-content: center;
				background: #eee;
				margin-right: 20upx;
				margin-bottom: 20upx;
				border-radius: 100upx;
				min-width: 60upx;
				height: 60upx;
				padding: 0 20upx;
				font-size: $font-base;
				color: $font-color-dark;
			}

			.selected {
				background: #fbebee;
				color: $uni-color-primary;
			}
		}

	}


	/* 规格选择弹窗 */
	.attr-content {
		padding: 10upx 30upx;

		.a-t {
			display: flex;

			image {
				width: 170upx;
				height: 170upx;
				flex-shrink: 0;
				margin-top: -40upx;
				border-radius: 8upx;
				;
			}

			.right {
				display: flex;
				flex-direction: column;
				padding-left: 24upx;
				font-size: $font-sm + 2upx;
				color: $font-color-base;
				line-height: 42upx;

				.price {
					font-size: $font-lg;
					color: $uni-color-primary;
					margin-bottom: 10upx;
				}

				.selected-text {
					margin-right: 10upx;
				}
			}
		}

		.attr-list {
			display: flex;
			flex-direction: column;
			font-size: $font-base + 2upx;
			color: $font-color-base;
			padding-top: 30upx;
			padding-left: 10upx;
		}

		.item-list {
			padding: 20upx 0 0;
			display: flex;
			flex-wrap: wrap;

			text {
				display: flex;
				align-items: center;
				justify-content: center;
				background: #eee;
				margin-right: 20upx;
				margin-bottom: 20upx;
				border-radius: 100upx;
				min-width: 60upx;
				height: 60upx;
				padding: 0 20upx;
				font-size: $font-base;
				color: $font-color-dark;
			}

			.selected {
				background: #fbebee;
				color: $uni-color-primary;
			}
		}
	}


	.popup {
		position: fixed;
		left: 0;
		top: 0;
		right: 0;
		bottom: 0;
		z-index: 99;

		&.show {
			display: block;

			.mask {
				animation: showPopup 0.2s linear both;
			}

			.layer {
				animation: showLayer 0.2s linear both;
			}
		}

		&.hide {
			.mask {
				animation: hidePopup 0.2s linear both;
			}

			.layer {
				animation: hideLayer 0.2s linear both;
			}
		}

		&.none {
			display: none;
		}

		.mask {
			position: fixed;
			top: 0;
			width: 100%;
			height: 100%;
			z-index: 1;
			background-color: rgba(0, 0, 0, 0.4);
		}

		.layer {
			position: fixed;
			z-index: 99;
			bottom: 0;
			width: 100%;
			min-height: 40vh;
			border-radius: 10upx 10upx 0 0;
			background-color: #fff;

			.btn {
				height: 66upx;
				line-height: 66upx;
				border-radius: 100upx;
				background: $uni-color-primary;
				font-size: $font-base + 2upx;
				color: #fff;
				margin: 30upx auto 20upx;
			}

			.to_bottom {
				height: 99upx;
				line-height: 99upx;
				margin: 30upx auto 20upx;
			}
		}

		@keyframes showPopup {
			0% {
				opacity: 0;
			}

			100% {
				opacity: 1;
			}
		}

		@keyframes hidePopup {
			0% {
				opacity: 1;
			}

			100% {
				opacity: 0;
			}
		}

		@keyframes showLayer {
			0% {
				transform: translateY(120%);
			}

			100% {
				transform: translateY(0%);
			}
		}

		@keyframes hideLayer {
			0% {
				transform: translateY(0);
			}

			100% {
				transform: translateY(120%);
			}
		}
	}

	/* 底部操作菜单 */
	/*.page-bottom {
		position: fixed;
		left: 15upx;
		bottom: 15upx;
		z-index: 10;
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
				
				background: transparent;
			}
		}
	}*/

	/* 底部操作菜单 */
	.page-bottom {
		position: fixed;
		left: 30upx;
		bottom: 30upx;
		z-index: 95;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 690upx;
		height: 100upx;
		background: rgba(255, 255, 255, .9);
		box-shadow: 0 0 20upx 0 rgba(0, 0, 0, .5);
		border-radius: 16upx;

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



	.goods-carts {
		left: 15upx;
		bottom: 30upx;
		z-index: 109;

		justify-content: center;
		align-items: center;
		width: 720upx;
		height: 100upx;
		background: rgba(255, 255, 255, .9);
		box-shadow: 0 0 20upx 0 rgba(0, 0, 0, .5);
		border-radius: 2upx;

		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */

		flex-direction: column;
		position: fixed;

	}

	.t-item {
		display: flex;
		position: relative;
		padding: 30upx 40upx;

		.image-wrapper {
			width: 180upx;
			height: 180upx;
			flex-shrink: 0;
			position: relative;
			background-size: 100% 100%;


		}

		.item-right {
			display: flex;
			flex-direction: column;
			flex: 1;
			overflow: hidden;
			position: relative;
			padding-left: 30upx;

			.title {
				font-size: $font-base - 4upx;
				color: $font-color-dark;
				height: 40upx;
				line-height: 40upx;

			}

			.price {
				font-size: $font-base - 2upx;
				color: $font-color-dark;
				height: 40upx;
				line-height: 40upx;

				&:before {
					content: '￥';
					font-size: $font-base - 2upx;
					//margin: 0 2upx 0 8upx;
				}
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

	.attributes_area {
		display: flex;
		flex-direction: column;
		flex: 1;
		overflow: hidden;
		position: relative;
		padding-left: 30upx;


		.attribute {
			display: flex;
			flex-direction: column;
			flex: 1;
			overflow: hidden;
			position: relative;
			padding-top: 20upx;
			padding-bottom: 20upx;


		}

		.attribute_button {
			/*display: flex;
			align-items: center;*/
			justify-content: center;
			width: 200upx;
			height: 80upx;
			font-size: $font-base;
			padding-top: 20upx;
			/*border-radius: 0;*/
			background: transparent;


		}
	}



	/* 分享 */
	.share-section {
		display: flex;
		align-items: center;
		color: $font-color-base;
		background: linear-gradient(left, #fdf5f6, #fbebf6);
		padding: 12upx 30upx;

		.share-icon {
			display: flex;
			align-items: center;
			width: 70upx;
			height: 30upx;
			line-height: 1;
			border: 1px solid $uni-color-primary;
			border-radius: 4upx;
			position: relative;
			overflow: hidden;
			font-size: 22upx;
			color: $uni-color-primary;

			&:after {
				content: '';
				width: 50upx;
				height: 50upx;
				border-radius: 50%;
				left: -20upx;
				top: -12upx;
				position: absolute;
				background: $uni-color-primary;
			}
		}

		.icon-xingxing {
			position: relative;
			z-index: 1;
			font-size: 24upx;
			margin-left: 2upx;
			margin-right: 10upx;
			color: #fff;
			line-height: 1;
		}

		.tit {
			font-size: $font-base;
			margin-left: 10upx;
		}

		.icon-bangzhu1 {
			padding: 10upx;
			font-size: 30upx;
			line-height: 1;
		}

		.share-btn {
			flex: 1;
			text-align: right;
			font-size: $font-sm;
			color: $uni-color-primary;
		}

		.icon-you {
			font-size: $font-sm;
			margin-left: 4upx;
			color: $uni-color-primary;
		}
	}
</style>
