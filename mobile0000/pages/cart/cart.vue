<template>
	<view class="container">
		<!-- 空白页 -->
		<view v-if="empty==true" class="empty">
			<image src="/static/emptyCart.jpg" mode="aspectFit"></image>
			<view v-if="empty" class="empty-tips">
				空空如也
				<view class="navigator" @click="navToShop">去购物</view>
			</view>
		</view>
		<view v-else>
			<!-- 列表 -->
			<!-- 列表 -->
			<view class="cart-list">
				<block v-for="(item, index) in cartList" :key="item.id">
					<view class="cart-item" :class="{'b-b': index!=cartList.length-1}">
						<view class="image-wrapper">
							<image :src="item.product.pic_url" :class="[item.loaded]" mode="aspectFill" lazy-load @load="onImageLoad('cartList', index)"></image>
							<view class="yticon icon-xuanzhong2 checkbox" :class="{checked: item.checked}" @click="check('item', index)"></view>
						</view>
						<view class="item-right">
							<text class="clamp title">{{item.product.name}}</text>
							<text v-if="role==2" class="price">¥{{item.product.purchase_price_register}}</text>
							<text v-if="role==5" class="price">¥{{item.product.purchase_price_corporate}}</text>
							<text v-if="role==1||role==0||role==3||role==4" class="price">¥{{item.product.retail_price}}</text>
							<uni-number-box class="step" :min=1 :max="item.product.stock" :value=item.quantity :index="index" @eventChange="numberChange"></uni-number-box>
						</view>
						<text class="del-btn yticon icon-fork" @click="deleteCartItem(index)"></text>
					</view>
				</block>
			</view>

			<!-- 底部菜单栏 -->
			<view class="action-section">
				<view class="checkbox">
					<image :src="allChecked?'/static/selected.png':'/static/select.png'" mode="aspectFit" @click="check('all')"></image>
					<view class="clear-btn" :class="{show: allChecked}" @click="clearCart">
						清空
					</view>
				</view>
				<view class="total-box">
					<text class="price">¥{{total}}</text>
					<text class="coupon">
						总价
					</text>
				</view>
				<button v-if="role==2 || role==5" type="primary" class="no-border confirm-btn" @click="goCreateOrder">去结算</button>


				<button v-else type="primary" class="no-border confirm-btn" @click="goCreateIntention">去下单</button>
			</view>
		</view>
	</view>
</template>

<script>
	import uniNumberBox from '@/components/uni-number-box.vue'
	export default {
		components: {
			uniNumberBox
		},
		data() {
			return {
				role: 0,
				quantity: 0,
				total: 0, //总价格
				allChecked: false, //全选状态  true|false
				empty: false, //空白页现实  true|false
				cartList: [],
			};
		},
		onShow() {
			var that = this;
			this.loadData();
		},
		onLoad() {},
		watch: {
			//显示空白页
			cartList(e) {
				let empty = e.length == 0 ? true : false;
				if (this.empty !== empty) {
					this.empty = empty;
				}
			}
		},
		methods: {
			//请求数据
			async loadData() {
				let that = this;
				let cart = uni.getStorageSync('cart');
				console.log(cart);
				that.cartList = cart;
				that.role = uni.getStorageSync("userDetail").flags;

			},
			//监听image加载完成
			onImageLoad(key, index) {
				this.$set(this[key][index], 'loaded', 'loaded');
			},
			//监听image加载失败
			onImageError(key, index) {
				this[key][index].image = '/static/errorImage.jpg';
			},
			//导向商品列表
			navToShop() {
				uni.switchTab({
					url: '/pages/category/category'
				});
			},
			//数量
			numberChange(data) {
				this.cartList[data.index].quantity = data.number;
				//更新storage
				this.calcTotal();
			},
			//选中状态处理
			check(type, index) {
				if (type == 'item') {
					this.cartList[index].checked = !this.cartList[index].checked;
				} else {
					const checked = !this.allChecked;
					const list = this.cartList;
					list.forEach(item => {
						item.checked = checked;
					})
					this.allChecked = checked;
				}
				this.calcTotal(type);
			},
			//删除
			deleteCartItem(index) {
				let list = this.cartList;
				let row = list[index];
				let id = row.id;
				//删除index
				this.cartList.splice(index, 1);
				this.calcTotal();
				uni.hideLoading();
			},
			//清空
			clearCart() {
				uni.showModal({
					content: '清空购物车？',
					success: (e) => {
						if (e.confirm) {
							this.cartList = [];
							uni.setStorageSync("cart", []);
						}
					}
				})
			},

			//计算总价
			calcTotal() {
				let list = this.cartList;
				if (list.length == 0) {
					this.empty = true;
					return;
				}
				let total = 0;
				let checked = true;

				list.forEach(item => {
					if (item.checked == true) {
						if (this.role == 2) {
							total += item.product.purchase_price_register * item.quantity;
						} else if (this.role == 5) {
							total += item.product.purchase_price_corporate * item.quantity;

						} else {
							total += item.product.retail_price * item.quantity;
						}

					} else if (checked == true) {
						checked = false;
					}
				})

				this.allChecked = checked;
				this.total = Number(total.toFixed(2));
			},

			//前往订单创建页面
			goCreateOrder() {

				let list = this.cartList;
				if (list.length == 0) {
					this.empty = true;
					return;
				}
				let total = 0;
				let quantity = 0;
				let credits = 0;
				let checked = true;
				var current_order = [];
				list.forEach(item => {
					if (item.checked == true) {
						quantity += item.quantity;
						if (this.role == 2) {
							total += item.product.purchase_price_register * item.quantity;
							credits += item.product.point * item.quantity;
						}
						if (this.role == 5) {
							total += item.product.purchase_price_corporate * item.quantity;
							credits += item.product.point * item.quantity;
						}
						current_order.push(item);
					} else if (checked == true) {
						checked = false;
					}
				})
				//this.allChecked = checked;
				this.total = Number(total.toFixed(2));
				console.log("这里是总数量" + quantity);
				this.quantity = quantity;
				uni.navigateTo({
					url: `/pages/order/createOrder?source=0&credits=${credits}&quantity=${quantity}&total=${total}&data=${encodeURIComponent(JSON.stringify(current_order))}`
				})

				this.allChecked = false;
				this.total = 0;
				uni.setStorageSync('cart', this.cartList);

			},
			//前往留言订单创建页面
			goCreateIntention() {
				let list = this.cartList;
				if (list.length == 0) {
					this.empty = true;
					return;
				}
				let total = 0;
				let quantity = 0;
				let checked = true;
				var current_intention = [];
				list.forEach(item => {
					if (item.checked == true) {
						total += item.product.retail_price * item.quantity;
						quantity += item.quantity;
						current_intention.push(item);
					} else if (checked == true) {
						checked = false;
					}
				})
				//this.allChecked = checked;
				total = Number(total.toFixed(2));
				console.log(this.total)
				uni.navigateTo({
					url: `/pages/order/createIntention?source=0&total=${total}&quantity=${quantity}&data=${encodeURIComponent(JSON.stringify(current_intention))}`
				})

				//删除购物车中的元素
				var i = this.cartList.length;
				while (i--) {
					if (this.cartList[i].checked == true) {
						console.log("删除了" + i);
						this.cartList.splice(i, 1);

					}
				}



				this.allChecked = false;
				this.total = 0;
				uni.setStorageSync('cart', this.cartList);


			}


		}
	}
</script>

<style lang='scss'>
	.container {
		padding-bottom: 134upx;

		/* 空白页 */
		.empty {
			position: fixed;
			left: 0;
			top: 0;
			width: 100%;
			height: 100vh;
			padding-bottom: 100upx;
			display: flex;
			justify-content: center;
			flex-direction: column;
			align-items: center;
			background: #fff;

			image {
				width: 240upx;
				height: 160upx;
				margin-bottom: 30upx;
			}

			.empty-tips {
				display: flex;
				font-size: $font-sm+2upx;
				color: $font-color-disabled;

				.navigator {
					color: $uni-color-primary;
					margin-left: 16upx;
				}
			}
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

	/* 底部栏 */
	.action-section {
		/* #ifdef H5 */
		margin-bottom: 100upx;
		/* #endif */
		position: fixed;
		left: 30upx;
		bottom: 30upx;
		z-index: 95;
		display: flex;
		align-items: center;
		width: 690upx;
		height: 100upx;
		padding: 0 30upx;
		background: rgba(255, 255, 255, .9);
		box-shadow: 0 0 20upx 0 rgba(0, 0, 0, .5);
		border-radius: 16upx;

		.checkbox {
			height: 52upx;
			position: relative;

			image {
				width: 52upx;
				height: 100%;
				position: relative;
				z-index: 5;
			}
		}

		.clear-btn {
			position: absolute;
			left: 26upx;
			top: 0;
			z-index: 4;
			width: 0;
			height: 52upx;
			line-height: 52upx;
			padding-left: 38upx;
			font-size: $font-base;
			color: #fff;
			background: $font-color-disabled;
			border-radius: 0 50px 50px 0;
			opacity: 0;
			transition: .2s;

			&.show {
				opacity: 1;
				width: 120upx;
			}
		}

		.total-box {
			flex: 1;
			display: flex;
			flex-direction: column;
			text-align: right;
			padding-right: 40upx;

			.price {
				font-size: $font-lg;
				color: $font-color-dark;
			}

			.coupon {
				font-size: $font-sm;
				color: $font-color-light;

				text {
					color: $font-color-dark;
				}
			}
		}

		.confirm-btn {
			padding: 0 38upx;
			margin: 0;
			border-radius: 100px;
			height: 76upx;
			line-height: 76upx;
			font-size: $font-base + 2upx;
			background: $uni-color-primary;
			box-shadow: 1px 2px 5px rgba(217, 60, 93, 0.72)
		}
	}

	/* 复选框选中状态 */
	.action-section .checkbox.checked,
	.cart-item .checkbox.checked {
		color: $uni-color-primary;
	}
</style>
