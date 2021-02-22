<template>
	<view class="container">
		<view class="wrapper">


			<uni-list>
				<uni-list-item :show-arrow="false" title="类别">
					<template v-slot:right="">
						<radio-group @change="radioChange">
							<radio value=0 :checked="accountData.flags === 1" />收入

							<radio value=1 :checked="accountData.flags === 0" />支出
						</radio-group>
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="金额">
					<template v-slot:right="">
						<input class="input" style="text-align:right" type="text" v-model="accountData.amount" placeholder-class="placeholder" />
					</template>
				</uni-list-item>
			</uni-list>

			<uni-list>
				<uni-list-item :show-arrow="false" title="描述">
					<template v-slot:right="">
						<input class="input" style="text-align:right" type="text" v-model="accountData.description" placeholder-class="placeholder" />
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list v-if="manageType==='edit'">
				<uni-list-item :show-arrow="false">
					<text class="txt" @click="deleteAccount(accountData.id)">删除该账目</text>
				</uni-list-item>
			</uni-list>


		</view>
		<button class="add-btn" @click="confirm">提交</button>
	</view>
</template>

<script>
	import uniList from '@/components/uni-list/uni-list.vue'
	import uniListItem from '@/components/uni-list-item/uni-list-item.vue'
	export default {
		components: {
			uniList,
			uniListItem
		},
		data() {
			return {
				user_id: 0,
				accountData: {
					id: 0,
					amount: 0,
					description: "记账",
					flags: 0,
					user: 0
				},
				manageType: 'edit'
			}
		},
		onLoad(option) {
			let title = '增加账目';
			this.user_id = uni.getStorageSync("userDetail").id;
			this.accountData.user = uni.getStorageSync("userDetail").id;
			if (option.type === 'edit') {
				title = '查看账目';
				this.accountData = JSON.parse(decodeURIComponent(option.data));
			}
			this.manageType = option.type;
			uni.setNavigationBarTitle({
				title
			})
		},
		methods: {
			//切换账目
			radioChange: function(evt) {
				this.accountData.flags = evt.target.value;
			},
			deleteAccount(id) {
				let that = this;
				uni.showModal({
					title: '提示',
					content: '确定要删除此记录吗？',
					success: function(res) {
						if (res.confirm) {
							that.util.request(that.api.ApiRoot + "users/" + uni.getStorageSync('userDetail').id + "/accounts/" + id + "/", {},
								'DELETE').then(function(res) {
								if (res.errno === 0) {
									uni.showToast({
										title: res.errMsg,
										duration: 2000
									})
									uni.navigateBack({});
								/*	uni.redirectTo({
											url: `/pages/account/account`,
											success() {
												var page = getCurrentPages().pop;
												if (page == undefined || page == null) return;
												page.onload();
											
										}
									
									})*/
								} else {
									uni.showModal({
										title: '提示',
										content: res.errMsg,
										success: function(res) {
											uni.redirectTo({
													url: `/pages/account/account`,
													success() {
														var page = getCurrentPages().pop;
														if (page == undefined || page == null) return;
														page.onload();
													
												}
											
											})
										}
									});

								}
							})
						} else if (res.cancel) {
							console.log('用户点击取消');
						}
					}
				});

			},

			//提交
			confirm() {
				let data = this.accountData;
				//验证金额
				if (!data.amount) {
					uni.showModal({
						title: '提示',
						content: '请填写金额',
						success: function(res) {}
					});
					return;
				}

				//验证编辑模式
				let that = this;
				if (that.manageType === "edit") {
					console.log(this.user_id)
					that.util.request(that.api.ApiRoot + "users/" + this.user_id + "/accounts/" + this.accountData.id + "/", {
						id: this.accountData.id,
						amount: this.accountData.amount,
						description: this.accountData.description,
						flags: this.accountData.flags,
						user: this.user_id
					}, 'PUT').then(function(res) {
							uni.showToast({
								title: res.errMsg,
								content: "已保存",
								duration: 2000
							});
                            uni.navigateBack({});
							//uni.redirect({
							//	url: '/pages/account/account'
							//})
					/*	uni.redirectTo({
									url: `/pages/account/account`,
									success() {
										var page = getCurrentPages().pop;
										if (page == undefined || page == null) return;
										page.onload();
									
								}

							})*/
					})

			} else {
				//发送请求  
				console.log(this.user_id)
				that.util.request(that.api.ApiRoot + "users/" + this.user_id + "/accounts/", {
					amount: this.accountData.amount,
					description: this.accountData.description,
					flags: this.accountData.flags,
					user: this.user_id

				}, 'POST').then(function(res) {
					uni.showToast({
						title: res.errMsg,
						content: "已保存",
						duration: 2000
					});

					uni.redirectTo({
							url: `/pages/account/account`,
							success() {
								var page = getCurrentPages().pop;
								if (page == undefined || page == null) return;
								page.onload();
							
						}
					
					})
				})
			}
		},


	}
	}
</script>

<style lang="scss">
	.wrapper {
		padding: 10upx;
		border-width: 1upx;
	}

	.editInfo_58 .main .editInfo_20 {
		white-space: normal;
		width: 685upx;
		height: 1upx;
		padding: 0upx;
		clear: both;
		margin-top: 42upx;
		margin-left: 32upx;
		float: left;
		text-align: left;
		border-radius: 0upx;
		font-size: 1upx;
		line-height: 1upx;
	}

	.editInfo_58 .main .editInfo_21 {
		white-space: normal;
		width: 684upx;
		height: 31upx;
		padding: 0upx;
		clear: both;
		margin-top: 50upx;
		margin-left: 30upx;
		float: left;
		text-align: left;
		border-radius: 0upx;
		font-size: 30upx;
		line-height: 31upx;
	}

	.editInfo_58 .main .editInfo_21 .title {
		white-space: normal;
		width: 103upx;
		height: 31upx;
		padding: 0upx;
		margin-top: 0upx;
		margin-left: 0upx;
		float: left;
		text-align: left;
		border-radius: 0upx;
		color: #ffffff;
		font-size: 29upx;
		line-height: 29upx;
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

	.txt {
		display: flex;
		justify-content: left;

		font-size: 30upx;
		color: rgba(170, 0, 0, 102);
	}
</style>
