<template>
	<view class="container">

		<view class="user-section">

			<view class="user-info-box">
				<view class="portrait-box">
					<image class="portrait" :src="userInfo.avatarUrl"></image>
				</view>
				<view class="info-box">
					<text class="username">{{userInfo.nickName}}</text>
				</view>
			</view>
			<view v-if="userDetail.flags==2" class="vip-card-box">
				<image class="card-bg" src="/static/vip-card-bg.png" mode=""></image>
				<!--<view class="b-btn">
					查看状态
				</view>-->
				<view class="tit">
					<text class="yticon icon-iLinkapp-"></text>
					开皇注册用户
				</view>
			</view>

			<view v-else class="vip-card-box">
				<image class="card-bg" src="/static/vip-card-bg.png" mode=""></image>
				<!--<view class="b-btn">
					去申请
				</view>-->
				<view class="tit">
					<text class="yticon icon-iLinkapp-" style="color: #555555;"></text>
					普通用户
				</view>

			</view>
		</view>

		<view class="cover-container" :style="[{
				transform: coverTransform,
				transition: coverTransition
			}]"
		 @touchstart="coverTouchstart" @touchmove="coverTouchmove" @touchend="coverTouchend">
			<image class="arc" src="/static/arc.png"></image>



			<view v-if="userDetail.flags == 1" class="tj-sction">
				<view class="tj-item">
					<text class="num">128.8</text>
					<text>余额</text>
				</view>
				<view class="tj-item">
					<text class="num">0</text>
					<text>优惠券</text>
				</view>
				<view class="tj-item">
					<text class="num">20</text>
					<text>积分</text>
				</view>
			</view>
			<view v-if="userDetail.flags == 2" class="tj-sction">
			     <view class="tj-item">
					<text class="num">0</text>
					<text>优惠券</text>
				</view>
				<view class="tj-item">
					<text class="num">20</text>
					<text>积分</text>
				</view>
			</view>



			<!-- 浏览历史 -->
			<view v-if="userDetail.flags == 2" class="history-section icon">
				<list-cell icon="icon-iconfontweixin" iconColor="#e07472" title="账本管理" @eventClick="navTo('/pages/account/account')"></list-cell>
				<list-cell icon="icon-dizhi" iconColor="#5fcda2" title="地址管理" @eventClick="navTo('/pages/address/address')"></list-cell>
				<list-cell icon="icon-share" iconColor="#9789f7" title="订单管理" @eventClick="navTo('/pages/order/order')"></list-cell>
				<list-cell icon="icon-pinglun-copy" iconColor="#ee883b" title="留言订单管理" @eventClick="navTo('/pages/intention/intention')"></list-cell>
				<list-cell icon="icon-shoucang_xuanzhongzhuangtai" conColor="#7178ee" title="申请管理" @eventClick="navTo('/pages/application/application')"></list-cell>
			</view>
			<view v-else class="history-section icon">
				<list-cell icon="icon-dizhi" iconColor="#5fcda2" title="地址管理" @eventClick="navTo('/pages/address/address')"></list-cell>
				<list-cell icon="icon-pinglun-copy" iconColor="#ee883b" title="留言订单管理" @eventClick="navTo('/pages/intention/intention_customer')"></list-cell>
				<list-cell icon="icon-shoucang_xuanzhongzhuangtai" iconColor="#7178ee" title="申请管理" @eventClick="navTo('/pages/application/application')"></list-cell>
			</view>



		</view>


	</view>
</template>
<script>
	import listCell from '@/components/mix-list-cell';

	let startY = 0,
		moveY = 0,
		pageAtTop = true;
	export default {
		components: {
			listCell
		},
		data() {
			return {
				coverTransform: 'translateY(0px)',
				coverTransition: '0s',
				moving: false,


				userInfo: {
					avatarUrl: "",
					nickName: ""
				},
				role: 0,
				role_sign: '',
				userDetail: {
					address_id: 0,
					email: "",
					flags: 0,
					gender: "",
					id: 0,
					mobile: "",
					name: "",
					phone: "",
					wx_avatar_url: "",
					wx_name: "",
					wx_open_id: "",
					wx_union_id: ""
				},

			}
		},
		onShow() {
			var that = this;
			that.userDetail = uni.getStorageSync('userDetail');
			that.role = uni.getStorageSync('userDetail').flags;
			console.log("role");
			if (that.role == 2) {
				this.role_sign = "开皇注册用户";
			} else {
				this.role_sign = "普通用户";
			}

			let term = uni.getStorageSync('userInfo');
			console.log(term);
			that.userInfo.avatarUrl = term.avatarUrl;
			that.userInfo.nickName = term.nickName;

		},
		// #ifndef MP
		onNavigationBarButtonTap(e) {
			const index = e.index;
			if (index === 0) {
				this.navTo('/pages/set/set');
			} else if (index === 1) {
				// #ifdef APP-PLUS
				const pages = getCurrentPages();
				const page = pages[pages.length - 1];
				const currentWebview = page.$getAppWebview();
				currentWebview.hideTitleNViewButtonRedDot({
					index
				});
				// #endif
				uni.navigateTo({
					url: '/pages/notice/notice'
				})
			}
		},
		// #endif

		methods: {

			/**
			 * 统一跳转接口,拦截未登录路由
			 * navigator标签现在默认没有转场动画，所以用view
			 */

			//导航
			navTo(res) {
				uni.navigateTo({
					url: res
				})

			},




			//获取库中的用户信息
			getMyData(openId) {
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "users/",
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


			coverTouchstart(e) {
				if (pageAtTop === false) {
					return;
				}
				this.coverTransition = 'transform .1s linear';
				startY = e.touches[0].clientY;
			},
			coverTouchmove(e) {
				moveY = e.touches[0].clientY;
				let moveDistance = moveY - startY;
				if (moveDistance < 0) {
					this.moving = false;
					return;
				}
				this.moving = true;
				if (moveDistance >= 80 && moveDistance < 100) {
					moveDistance = 80;
				}

				if (moveDistance > 0 && moveDistance <= 80) {
					this.coverTransform = `translateY(${moveDistance}px)`;
				}
			},
			coverTouchend() {
				if (this.moving === false) {
					return;
				}
				this.moving = false;
				this.coverTransition = 'transform 0.3s cubic-bezier(.21,1.93,.53,.64)';
				this.coverTransform = 'translateY(0px)';
			}
		}
	}
</script>
<style lang='scss'>
	%flex-center {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	%section {
		display: flex;
		justify-content: space-around;
		align-content: center;
		background: #fff;
		border-radius: 10upx;
	}

	.user-section {
		height: 520upx;
		padding: 100upx 30upx 0;
		position: relative;
		background-color: #F0AD4E;

		.bg {
			position: absolute;
			left: 0;
			top: 0;
			width: 100%;
			height: 100%;
			filter: blur(1px);
			opacity: .7;
		}
	}

	.user-info-box {
		height: 180upx;
		display: flex;
		align-items: center;
		position: relative;
		z-index: 1;

		.portrait {
			width: 130upx;
			height: 130upx;
			border: 5upx solid #fff;
			border-radius: 50%;
		}

		.username {
			font-size: $font-lg + 6upx;
			color: $font-color-dark;
			margin-left: 20upx;
		}
	}

	.vip-card-box {
		display: flex;
		flex-direction: column;
		color: #f7d680;
		height: 240upx;
		background: linear-gradient(left, rgba(0, 0, 0, .7), rgba(0, 0, 0, .8));
		border-radius: 16upx 16upx 0 0;
		overflow: hidden;
		position: relative;
		padding: 20upx 24upx;

		.card-bg {
			position: absolute;
			top: 20upx;
			right: 0;
			width: 380upx;
			height: 260upx;
		}

		.b-btn {
			position: absolute;
			right: 20upx;
			top: 16upx;
			width: 132upx;
			height: 40upx;
			text-align: center;
			line-height: 40upx;
			font-size: 22upx;
			color: #36343c;
			border-radius: 20px;
			background: linear-gradient(left, #f9e6af, #ffd465);
			z-index: 1;
		}

		.tit {
			font-size: $font-base+2upx;
			color: #f7d680;
			margin-bottom: 28upx;

			.yticon {
				color: #f6e5a3;
				margin-right: 16upx;
			}
		}

		.e-b {
			font-size: $font-sm;
			color: #d8cba9;
			margin-top: 10upx;
		}
	}

	.cover-container {
		background: $page-color-base;
		margin-top: -150upx;
		padding: 0 30upx;
		position: relative;
		background: #f5f5f5;
		padding-bottom: 20upx;

		.arc {
			position: absolute;
			left: 0;
			top: -34upx;
			width: 100%;
			height: 36upx;
		}
	}

	.tj-sction {
		@extend %section;

		.tj-item {
			@extend %flex-center;
			flex-direction: column;
			height: 140upx;
			font-size: $font-sm;
			color: #75787d;
		}

		.num {
			font-size: $font-lg;
			color: $font-color-dark;
			margin-bottom: 8upx;
		}
	}

	.order-section {
		@extend %section;
		padding: 28upx 0;
		margin-top: 20upx;

		.order-item {
			@extend %flex-center;
			width: 120upx;
			height: 120upx;
			border-radius: 10upx;
			font-size: $font-sm;
			color: $font-color-dark;
		}

		.yticon {
			font-size: 48upx;
			margin-bottom: 18upx;
			color: #fa436a;
		}

		.icon-shouhoutuikuan {
			font-size: 44upx;
		}
	}

	.history-section {
		padding: 0upx 0 0;
		margin-top: 40upx;
		background: #fff;
		border-radius: 10upx;

		/*	.sec-header {
			display: flex;
			align-items: center;
			font-size: $font-base;
			color: $font-color-dark;
			line-height: 0upx;
			margin-left: 30upx;

			.yticon {
				font-size: 44upx;
				color: #5eba8f;
				margin-right: 16upx;
				line-height: 40upx;
			}
		}*/

		.h-list {
			white-space: nowrap;
			padding: 30upx 30upx 0;

			image {
				display: inline-block;
				width: 160upx;
				height: 160upx;
				margin-right: 20upx;
				border-radius: 10upx;
			}
		}
	}
</style>
