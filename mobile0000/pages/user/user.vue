<template>
	<view class="container">
		<view class="user-section">
			<view class="user-info-box">
				<view class="portrait-box" @click="naviToSettings()">
					<image class="portrait" :src="userInfo.avatarUrl"></image>
				</view>
				<view class="info-box">
					<text class="username">{{userInfo.nickName}}</text>
					<text class="role">{{role_sign}}</text>
				</view>
			</view>
		</view>

		<view class="cover-container" :style="[{
				transform: coverTransform,
				transition: coverTransition
			}]"
		 @touchstart="coverTouchstart" @touchmove="coverTouchmove" @touchend="coverTouchend">


			<!-- 功能页面跳转 -->
			<view v-if="userDetail.flags == 2" class="history-section icon">
				<list-cell icon="icon-shouye" iconColor="#5fcda2" title="订单管理" @eventClick="navTo('/pages/order/order')"></list-cell>
				<list-cell icon="icon-xiaoxi" iconColor="#5fcda2" title="留言订单管理" @eventClick="navTo('/pages/intention/intention')"></list-cell>
				<list-cell icon="icon-dizhi" iconColor="#5fcda2" title="地址管理" @eventClick="navTo('/pages/address/address')"></list-cell>
				<list-cell icon="icon-tuijian" iconColor="#5fcda2" title="申请管理" @eventClick="navTo('/pages/application/application')"></list-cell>
				<list-cell icon="icon-daifukuan" iconColor="#5fcda2" title="账本管理" @eventClick="navTo('/pages/account/account')"></list-cell>
			</view>
			<view v-else class="history-section icon">
				<list-cell icon="icon-xiaoxi" iconColor="#5fcda2" title="留言订单管理" @eventClick="navTo('/pages/intention/intention_customer')"></list-cell>
				<list-cell icon="icon-dizhi" iconColor="#5fcda2" title="地址管理" @eventClick="navTo('/pages/address/address')"></list-cell>
				<list-cell icon="icon-tuijian" iconColor="#5fcda2" title="申请管理" @eventClick="navTo('/pages/application/application')"></list-cell>
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

				coverTransform: 'translateY(0px)',
				coverTransition: '0s',
				moving: false,

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
			if (index == 0) {
				this.navTo('/pages/set/set');
			} else if (index == 1) {
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
			//导航
			navTo(res) {
				uni.navigateTo({
					url: res
				})

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
		height: 400upx;
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


	.cover-container {
		/*background: $page-color-base;*/

		margin-top: 50upx;
		/*padding: 30 30upx;*/
		position: relative;
		background: #f5f5f5;
		padding-bottom: 20upx;
		border-radius: 20rpx;
		margin: 30rpx 20rpx 30rpx 20rpx;

	}


	.history-section {
		/*padding: 30upx 0 0;
		margin-top: 50upx;*/
		background: #fff;
		/*border-radius: 10upx;*/
		border-radius: 20rpx;
		margin: 30rpx 20rpx 30rpx 20rpx;
		align-items: center;


		.sec-header {
			display: flex;
			align-items: center;
			font-size: $font-base;
			color: $font-color-dark;
			line-height: 40upx;
			margin-left: 30upx;

			align-items: center;

			.yticon {
				font-size: 44upx;
				color: #5eba8f;
				margin-right: 16upx;
				line-height: 40upx;
			}
		}

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
