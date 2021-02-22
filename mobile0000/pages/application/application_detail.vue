<template>
	<view class="container">
		<view class="wrapper">
			<uni-list>
				<uni-list-item :show-arrow="false" title="姓名" :rightText="applicationData.name">

				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="性别" :rightText="applicationData.gender">


				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="联系方式" :rightText="applicationData.phone">

				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="邮箱" :rightText="applicationData.email">
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="证件正面照">
					<template v-slot:right="">
						<image style="width: 40px;height: 40px;" :src="applicationData.idc_front_pic_url" mode="widthFix"></image>
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="证件反面照">
					<template v-slot:right="">
						<image style="width: 40px;height: 40px;" :src="applicationData.idc_back_pic_url" mode="widthFix"></image>
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list v-if="applicationData.flags==2">
				<uni-list-item :show-arrow="false" title="拒绝原因" :rightText="applicationData.reason_of_refusal">

				</uni-list-item>
			</uni-list>
		</view>
		<button v-if="applicationData.flags ==0" class="add-btn" @click="manageApplication('edit')">修改申请信息</button>
		
		<button v-if="applicationData.flags ==1 & userInfo.flags ==2" class="add-btn" disabled="true">申请已通过</button>
		<button v-if="applicationData.flags ==1 & userInfo.flags !==2" class="add-btn" @click="signContract()">签署协议</button>
		<button v-if="applicationData.flags ==2" class="add-btn" disabled="true">申请被拒绝</button>


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
				applicationData: {
					id: 0,
					created_at: "",
					name: "",
					gender: "",
					phone: "",
					email: "",
					ip: "",
					idc_front_pic_url: "",
					idc_back_pic_url: "",
					reason_of_refusal: null,
					flags: 0,
					user: 0
				},
				userInfo: {}

			}
		},
		onLoad(option) {
			var appData = JSON.parse(decodeURIComponent(option.data));
			this.applicationData = appData;
			this.userInfo = uni.getStorageSync('userDetail');

		},


		methods: {
			//切换性别
			radioChange: function(evt) {
				this.applicationData.gender = evt.target.value;
			},
			//提交
			manageApplication(type) {
				var data = this.applicationData;
				uni.navigateTo({
					url: `/pages/application/manageApplication?type=${type}&data=${encodeURIComponent(JSON.stringify(data))}`
				})
			},

			signContract() {
				uni.showModal({
					title: "恭喜你",
					content: "您的申请已经通过开皇工作人员的审核，在确定获得开皇注册用户的身份之前，请充分阅读以下的合作条款。/n 若同意以上条款，点击同意即可成为开皇社区注册用户！",
					showCancel: true,
					confirmText: "确定",
					cancelText: "取消",
					success: function(res) {
						if (res.confirm) {
							uni.getStorageSync("userDetail").flags = 2;
							uni.request({
								header: {
									"content-type": "application/json"
								},
								url: "https://api.kaihuangliulian.com/v1/users/" + uni.getStorageSync("userDetail").id + "/",
								data: uni.getStorageSync("userDetail"),
								method: "PUT",
								success(res) {
									uni.showModal({
										title: "通知",
										content: "权限更新成功，退出重新登录即可以体验",
										showCancel: false,
										confirmText: "确定"
									})

								},
								fail(res) {
									console.log(res);
								}
							})
						}
					}

				})

			},
			changeImg() {
				uni.chooseImage({
					success: (chooseImageRes) => {
						const tempFilePaths = chooseImageRes.tempFilePaths;
						this.changeimg = tempFilePaths[0];
						console.log(this.changeImg);
						let open_id = uni.getStorageSync('userDetail').open_id;
						console.log(open_id);
						//上传图片	
						let that = this;
						that.util.request(that.api.ApiRoot + 'upload?' + 'image=' + this.changeimg + '&open_id=', 'POST', {
							"content-type": "multipart/form-data"
						}).then();
					}
				});
			}
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
</style>
