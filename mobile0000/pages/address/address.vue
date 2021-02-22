<template>
	<view class="content b-t">
		<view class="list b-b" v-for="(item, index) in addressList" :key="index" @click="checkAddress(item)">

			<view class="wrapper">
				<view class="address-box">
					<text v-if="default_address==item.id" class="tag">默认</text>
					<text class="name">{{item.contact_name}} {{item.contact_phone}} </text>
				</view>
				<view class="u-box">
					<text class="address">{{item.province}} {{item.city}} {{item.address}}</text>
				</view>


			</view>

			<text class="yticon icon-bianji" @click.stop="addAddress('edit', item)"></text>
		</view>
		<button class="add-btn" @click="addAddress('add')">新增地址</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				source: 0,
				default_address: 0,
				addressList: []
			}
		},
		onShow() {
			this.getAddressList();
		},
		onLoad(options) {
			this.source = options.source;
			this.default_address = uni.getStorageSync("userDetail").address_id;
		},
		methods: {
			deleteAddress(id) {
				let that = this;
				uni.showModal({
					title: '提示',
					content: '确定要删除此记录吗？',
					success: function(res) {
						if (res.confirm) {
							that.utils.request("users/" + uni.getStorageSync('userDetail').id + "/addresses",
								'DELETE').then(function(res) {
								if (res.errno === 0) {
									uni.showToast({
										title: res.errMsg,
										duration: 2000
									});
									that.getAddressList()
								} else {
									uni.showModal({
										title: '提示',
										content: res.errMsg,
										success: function(res) {}
									});
								}
							})
						} else if (res.cancel) {
							console.log('用户点击取消');
						}
					}
				});

			},
			getAddressList() {
				let that = this;
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "users/" + uni.getStorageSync('userDetail').id + "/addresses/",

						method: "GET",
						success(res) {
							resolve(res.data);
							that.addressList = res.data;
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});
			},
			//选择地址
			checkAddress(item) {
				if (this.source == 1) {
					uni.setStorageSync('selected_address', item)
					uni.navigateBack()
				}
			},
			addAddress(type, item) {
				uni.navigateTo({
					url: `/pages/address/addressManage?type=${type}&data=${JSON.stringify(item)}`
				})
			}
		}
	}
</script>

<style lang='scss'>
	page {
		padding-bottom: 120upx;
	}

	.content {
		position: relative;
	}

	.list {
		display: flex;
		align-items: center;
		padding: 20upx 30upx;
		position: relative;
		border-radius: 20rpx;
		margin: 30rpx 20rpx 30rpx 20rpx;
	}

	.wrapper {
		display: flex;
		margin-top: 16upx;
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

		.address {
			font-size: 30upx;
			color: $font-color-dark;
		}
	}

	.u-box {
		font-size: 28upx;
		color: $font-color-light;
		margin-top: 16upx;

		.name {
			margin-right: 30upx;
		}
	}

	.icon-bianji {
		display: flex;
		align-items: center;
		height: 80upx;
		font-size: 40upx;
		color: $font-color-light;
		padding-left: 30upx;
	}

	.add-btn {
		position: fixed;
		left: 30upx;
		right: 30upx;
		bottom: 16upx;
		z-index: 95;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 690upx;
		height: 80upx;
		font-size: 32upx;
		color: #fff;
		background-color: $base-color;
		border-radius: 10upx;
		box-shadow: 1px 2px 5px rgba(219, 63, 96, 0.4);
	}
</style>
