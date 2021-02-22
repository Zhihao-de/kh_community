<template>
	<view class="content">
		<!--<view class='box' v-if="flag==0">-->
		<image v-if="flag==0" :src="sub_imageSrc" :mode="aspectFit" @click="chooseImage()" />
		<!--</view>
		<view class='box' v-else>-->
		<image v-else :src='imageSrc' :mode="aspectFit" @click="chooseImage()" />
		<!--</view>-->
	</view>
</template>
<script>
	import uniList from '@/components/uni-list/uni-list.vue'
	import uniListItem from '@/components/uni-list-item/uni-list-item.vue'
	import permision from "@/common/permission.js"

	var sourceType = [
		['camera'],
		['album'],
		['camera', 'album']
	]
	var sizeType = [
		['compressed'],
		['original'],
		['compressed', 'original']
	]
	export default {
		data() {
			return {
				flag: 0,
				title: '上传证件正面照',
				imageSrc: "",
				sub_imageSrc: "/static/missing-face.png",
				imageList: [],
				sourceTypeIndex: 2,
				sourceType: ['拍照', '相册', '拍照或相册'],
				sizeTypeIndex: 2,
				sizeType: ['压缩', '原图', '压缩或原图'],
				countIndex: 0,

			}
		},
		onUnload() {
			this.imageList = [],
				this.imageFile = '',
				this.sourceTypeIndex = 2,
				this.sourceType = ['拍照', '相册', '拍照或相册'],
				this.sizeTypeIndex = 2,
				this.sizeType = ['压缩', '原图', '压缩或原图'],
				this.countIndex = 0;
		},
		methods: {
			onLoad(option) {
				var url = option.img_url;

				if (url == '') {
					this.flag = 0;
				} else {
					this.flag = 1;
					this.imageList.push(url);
					this.imageSrc = url;
				}
			},
			sourceTypeChange: function(e) {
				this.sourceTypeIndex = parseInt(e.detail.value)
			},
			sizeTypeChange: function(e) {
				this.sizeTypeIndex = parseInt(e.detail.value)
			},
			countChange: function(e) {
				this.countIndex = e.detail.value;
			},
			chooseImage: async function() {
				// #ifdef APP-PLUS
				// TODO 选择相机或相册时 需要弹出actionsheet，目前无法获得是相机还是相册，在失败回调中处理
				if (this.sourceTypeIndex !== 2) {
					let status = await this.checkPermission();
					if (status !== 1) {
						return;
					}
				}
				// #endif
				if (this.imageList.length === 9) {
					let isContinue = await this.isFullImg();
					console.log("是否继续?", isContinue);
					if (!isContinue) {
						return;
					}
				}
				uni.chooseImage({
					sourceType: sourceType[this.sourceTypeIndex],
					//sizeType: sizeType[this.sizeTypeIndex],
					sizeType: ['compressed'],
					count: 1,
					sourceType: ['album'],

					success: (chooseImageRes) => {
						const tempFilePaths = chooseImageRes.tempFilePaths;
						let changeImg = tempFilePaths[0];
						console.log(changeImg);
						let open_id = uni.getStorageSync('userDetail').wx_open_id;
						console.log(open_id);
						//上传图片	
						let that = this;

						uni.uploadFile({
							url: "https://api.kaihuangliulian.com/v1/upload",
							filePath: changeImg,
							name: "image",
							formData: {
								"open_id": uni.getStorageSync('userDetail').wx_open_id,
								"image": changeImg
							},
							success: (uploadFileRes) => {

								console.log(uploadFileRes);
								var term = JSON.parse(uploadFileRes.data);
								that.flag = 1;
								that.imageList[0] = term.url;
								var pages = getCurrentPages();
								var prepage = pages[pages.length - 2]; //上一个页面
								prepage.$vm.applicationData.idc_front_pic_url = term.url;
								uni.navigateBack()
							}
						})

					},


					fail: (err) => {
						// #ifdef APP-PLUS
						if (err['code'] && err.code !== 0 && this.sourceTypeIndex === 2) {
							this.checkPermission(err.code);
						}
						// #endif
						// #ifdef MP
						uni.getSetting({
							success: (res) => {
								let authStatus = false;
								switch (this.sourceTypeIndex) {
									case 0:
										authStatus = res.authSetting['scope.camera'];
										break;
									case 1:
										authStatus = res.authSetting['scope.album'];
										break;
									case 2:
										authStatus = res.authSetting['scope.album'] && res.authSetting['scope.camera'];
										break;
									default:
										break;
								}
								if (!authStatus) {
									uni.showModal({
										title: '授权失败',
										content: 'Hello uni-app需要从您的相机或相册获取图片，请在设置界面打开相关权限',
										success: (res) => {
											if (res.confirm) {
												uni.openSetting()
											}
										}
									})
								}
							}
						})
						// #endif
					}
				})
			},

			previewImage: function(e) {
				var current = e.target.dataset.src
				uni.previewImage({
					current: current,
					urls: this.imageList,
					longPressActions: {
						itemList: ['发送给朋友', '保存图片', '收藏'],
						success: function(data) {
							console.log('选中了第' + (data.tapIndex + 1) + '个按钮,第' + (data.index + 1) + '张图片');
						},
						fail: function(err) {
							console.log(err.errMsg);
						}
					}
				})
			},
			async checkPermission(code) {
				let type = code ? code - 1 : this.sourceTypeIndex;
				let status = permision.isIOS ? await permision.requestIOS(sourceType[type][0]) :
					await permision.requestAndroid(type === 0 ? 'android.permission.CAMERA' :
						'android.permission.READ_EXTERNAL_STORAGE');
				if (status === null || status === 1) {
					status = 1;
				} else {
					uni.showModal({
						content: "没有开启权限",
						confirmText: "设置",
						success: function(res) {
							if (res.confirm) {
								permision.gotoAppSetting();
							}
						}
					})
				}
				return status;
			}
		}
	}
</script>
<style>
	page {
		background-color: #000000;
		align-items: center;
		display: flex;
		flex-direction: column;

		justify-content: center;
	}

	.content {

		background-color: #999999;

		justify-content: center;
		display: flex;
		align-items: center;
	}

	.box {
		width: 40%;
		height: 90%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
