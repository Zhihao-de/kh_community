<template>
	<view class="container">
		<view class="wrapper">
			<uni-list>
				<uni-list-item :show-arrow="false" title="姓名">
					<template v-slot:right="">
						<input class="input" style="text-align:right" type="text" v-model="applicationData.name" placeholder-class="placeholder" />
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="性别">
					<template v-slot:right="">
						<radio-group @change="radioChange">
							<radio value="男" :checked="applicationData.gender === '男'" />男

							<radio value="女" :checked="applicationData.gender === '女'" />女
						</radio-group>
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="联系方式">
					<template v-slot:right="">
						<input class="input" style="text-align:right" type="text" v-model="applicationData.phone" placeholder-class="placeholder" />
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item :show-arrow="false" title="邮箱">
					<template v-slot:right="">
						<input class="input" style="text-align:right" type="text" v-model="applicationData.email" placeholder-class="placeholder" />
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item title="证件正面照" @click="navToPicFront(applicationData.idc_front_pic_url)">
					<template v-slot:right="">
						<image style="width: 40px;height: 40px;" :src="applicationData.idc_front_pic_url" mode="widthFix"></image>
					</template>
				</uni-list-item>
			</uni-list>
			<uni-list>
				<uni-list-item title="证件反面照" @click="navToPicBack(applicationData.idc_back_pic_url)">
					<template v-slot:right="">
						<image style="width: 40px;height: 40px;" :src="applicationData.idc_back_pic_url" mode="widthFix"></image>
					</template>
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
				manageType: 'edit'
			}
		},
		onLoad(option) {
			let title = '新增申请';
			this.user_id = uni.getStorageSync("userDetail").id;

			if (option.type === 'edit') {
				title = '编辑申请';
				console.log(option);
				this.applicationData = JSON.parse(decodeURIComponent(option.data));
			}
			this.manageType = option.type;
			uni.setNavigationBarTitle({
				title
			})
		},


		methods: {
			//切换性别
			radioChange: function(evt) {
				this.applicationData.gender = evt.target.value;
			},
			//提交
			confirm() {
				let data = this.applicationData;
				//验证姓名
				if (!data.name) {
					uni.showModal({
						title: '提示',
						content: '请填写姓名',
						success: function(res) {}
					});
					return;
				}
				//验证电话号码
				if (!/(^1[3|4|5|7|8][0-9]{9}$)/.test(data.phone)) {
					uni.showModal({
						title: '提示',
						content: '请输入正确的手机号码',
						success: function(res) {}
					});
					return;
				}
				//验证编辑模式
				let that = this;
				if (that.manageType == "edit") {
					that.util.request(that.api.ApiRoot + "users/" + this.user_id + "/applications/" + this.applicationData.id + "/",
						data, 'PUT').then(function(res) {
						uni.showToast({
							title: res.errMsg,
							content: "已保存",
							duration: 2000
						});
						uni.navigateBack();
					})

				} else {
					//发送请求
					let that = this;
					that.util.request(that.api.ApiRoot + "users/" + this.user_id + "/applications/", {
						name: this.applicationData.name,
						gender: this.applicationData.gender,
						phone: this.applicationData.phone,
						email: this.applicationData.email,
						ip: "0.0.0.0",
						idc_front_pic_url: this.applicationData.idc_front_pic_url,
						idc_back_pic_url: this.applicationData.idc_back_pic_url,
						flags: 0,
						user: uni.getStorageSync("userDetail").id
					}, 'POST').then(function(res) {
						//uni.setStorageSync("userDetail", user_info);
						uni.showToast({
							title: res.errMsg,
							content: "已保存",
							duration: 2000
						});
						uni.navigateBack();
					})
				}
			},
			navToPicFront(res) {
				uni.navigateTo({
					url: `/pages/application/picFront?img_url=${res}`
				})
			},
			navToPicBack(res) {
				uni.navigateTo({
					url: `/pages/application/picBack?img_url=${res}`
				})
			},
			preview() {
				uni.previewImage({
					current: '0',
					urls: [""],
					longPressActions: {
						itemList: ['保存图片'],
						success: function(data) {
							console.log('选中了第' + (data.tapIndex + 1) + '个按钮,第' + (data.index + 1) + '张图片');
						},
						fail: function(err) {
							console.log(err.errMsg);
						}
					}
				});
			},
			changeImg() {
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
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
						console.log("nnnnnnnnnnnnnnnnnnnnnnnnn")
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
