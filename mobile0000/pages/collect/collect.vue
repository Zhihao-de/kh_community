

<script>
	export default {
		data() {
			return {
				collect_list: []
			}
		},
		onLoad:function(){
			this.getCollectList()
			console.log(111)
		},
		methods: {
			getCollectList(){
				let that = this
				that.util.request(that.api.CollectList).then(function(res) {
					that.collect_list = res.data.collect_list
					console.log(that.collect_list)
					
				})
			},
			toProduct(goods_id){
				uni.navigateTo({
				    url: '/pages/product/product?id='+goods_id
				});
			},
			deleteColect(goods_id){
				
				let that = this
				uni.showModal({
				    title: '提示',
				    content: '确定要删除此收藏吗？',
				    success: function (res) {
				        if (res.confirm) {
				            that.util.request(that.api.CollectAdd, {goods_id: goods_id}).then(function(res) {
				            	if (res.errno === 0){
				            		uni.showToast({
				            		    title: res.errMsg,
				            		    duration: 2000
				            		});
									that.getCollectList()
				            	}else{
				            		uni.showModal({
				            		    title: '提示',
				            		    content: res.errMsg,
				            		    success: function (res) {
				            		    }
				            		});
				            	}
				            })
				        } else if (res.cancel) {
				            console.log('用户点击取消');
				        }
				    }
				});
				
			}
		}
	}
</script>

<style lang='scss'>
	.container {
		width: 100%;
		height: auto;
		.no-collect {
			color: #999999;
			text-align: center;
		}
		.collect-list {
			width: 100%;
			.item {
				display: flex;
				margin-top: 20upx;
				padding: 12upx;
				border-bottom: 2upx solid #C0C4CC;
				.img{
					flex: 0 0 150upx;
					width: 150upx;
					height: 150upx;
					border-radius: 20upx;
				}
				.info{
					flex: 1;
					padding: 0 20upx;
					.name {
						color: #888;
						line-height: 40upx;
					}
					.price {
						color: #DD524D;
						margin-top: 15upx;
						line-height: 40upx;
					}
				}
			}
		}
	}
</style>
