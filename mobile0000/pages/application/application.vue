<template>
	<view class="content b-t">
		<view>
			<uni-list v-for="item in applicationList" :key="item.id">
				<view @click="naviToDetail(item)">
					<uni-list-item :title="item.name" :note="item.created_at" :showArrow="false">
						<template v-slot:right="">
							<text :style="{color: item.flagsTipColor}">{{item.flagsTip}}</text>
						</template>
					</uni-list-item>
				</view>
			</uni-list>
		</view>

		<button class="add-btn" v-if="role !==2" @click="manageApplication('add',item)">申请成为开皇社区人员</button>
	</view>
</template>

<script>
	import uniList from '@/components/uni-list/uni-list.vue';
	import uniListItem from '@/components/uni-list-item/uni-list-item.vue';

	export default {
		components: {
			uniList,
			uniListItem
		},
		data() {
			return {
				source: 0,
				flags: 0,
				role: 0,
				applicationList: []
			}
		},
		onShow() {},
		onLoad(option) {
			this.loadData();
			this.source = option.source;
			this.role = uni.getStorageSync('userDetail').flags;
		},
		methods: {
			async loadData() {
				//初始化申请列表  一个用户下可能有多个申请
				var applications = await this.getApplication();
				this.applicationList = applications;
				console.log(this.applicationList);
				applications = applications.filter(item => {
					item = Object.assign(item, this.applicationflagsExp(item.flags));
				});
			},

			//订单状态文字和颜色
			applicationflagsExp(flags) {
				let flagsTip = '',
					flagsTipColor = '#fa436a';
				switch (+flags) {
					case 0:
						flagsTip = '待审批';
						flagsTipColor = '#ffcc66';
						break;
					case 1:
						flagsTip = '同意';
						flagsTipColor = '#00ff00';
						break;
					case 2:
						flagsTip = '不同意';
						flagsTipColor = '#ff0000';
						break;

				}
				return {
					flagsTip,
					flagsTipColor
				};
			},

			getApplication() {
				let that = this;
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "users/" + uni.getStorageSync("userDetail").id + "/applications/",

						method: "GET",
						success(res) {
							resolve(res.data);
							console.log(res.data);
						},
						fail(res) {
							console.log(res);
						}
					})
				}).catch((e) => {});
			},

			manageApplication(type, item) {
				uni.navigateTo({
					url: `/pages/application/manageApplication?type=add&data=${encodeURIComponent(JSON.stringify(item))}`
				})
			},


			naviToDetail(item) {
				uni.navigateTo({
					url: `/pages/application/application_detail?data=${encodeURIComponent(JSON.stringify(item))}`
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
		;
		background: #fff;
		position: relative;
	}

	.row {
		display: flex;
		align-items: center;
		position: relative;
		padding: 0 30upx;
		height: 110upx;
		background: #fff;

		.tit {
			flex-shrink: 0;
			width: 200upx;
			font-size: 30upx;
			color: $font-color-dark;
		}

		.text {
			flex: 1;
			font-size: 30upx;
			color: $font-color-dark;
		}

		.image {
			margin: 40upx 0;
			width: 200rpx;
		}


		.icon-shouhuodizhi {
			font-size: 36upx;
			color: $font-color-light;
		}
	}

	.wrapper {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.application-box {
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

		.application-main {
			font-weight: bold;
			font-size: 30upx;
			color: $font-color-dark;
		}

		.application-area {
			font-size: 30upx;
			color: $font-color-dark;
		}

		.application-postcode {
			font-size: 20upx;
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

	.del-btn {
		padding: 4upx 10upx;
		font-size: 34upx;
		height: 50upx;
		color: $font-color-light;
	}


	.cart-item {
		display: flex;
		position: relative;
		padding: 30upx 40upx;


		.top {
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

		}

		.item-right {
			display: flex;
			flex-direction: column;
			flex: 1;
			overflow: hidden;
			position: relative;
			padding-left: 30upx;

			.price {
				font-size: $font-base + 2upx;
				color: $font-color-dark;
				height: 40upx;
				line-height: 40upx;
			}

			.time {
				font-size: $font-base;
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

			/*	.price {
				height: 50upx;
				line-height: 50upx;
			}*/
		}

		.del-btn {
			padding: 4upx 10upx;
			font-size: 34upx;
			height: 50upx;
			color: $font-color-light;
		}
	}
</style>
