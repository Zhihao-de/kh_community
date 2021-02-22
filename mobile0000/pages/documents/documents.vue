<template>
	<view>
		<web-view :webview-styles="webviewStyles" src="https://www.sf-express.com/us/sc/dynamic_function/price/"></web-view>

	</view>
</template>
<script>
	export default {
		data() {
			return {
				title: 'downloadFile',
				imageSrc: ''
			}
		},
		onUnload() {
			this.imageSrc = '';
		},
		methods: {
			downloadImage: function() {
				uni.showLoading({
					title: '下载中'
				})
				var self = this
				uni.downloadFile({
					url: "https://img-cdn-qiniu.dcloud.net.cn/uniapp/images/uni@2x.png",
					success: (res) => {
						console.log('downloadFile success, res is', res)
						self.imageSrc = res.tempFilePath;
						uni.hideLoading();
					},
					fail: (err) => {
						console.log('downloadFile fail, err is:', err)
					}
				})
			}
		}
	}
</script>

<style>
	.img {
		width: 500rpx;
		height: 500rpx;
		margin: 0 95rpx;
	}
</style>
