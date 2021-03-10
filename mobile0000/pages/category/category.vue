<template>
	<view class="content">
		<scroll-view scroll-y class="left-aside">
			<view v-for="item in flist" :key="item.id" class="f-item b-b" :class="{ active: item.id === currentId }" @click="tabtap(item)">{{ item.name }}</view>
		</scroll-view>
		<scroll-view scroll-with-animation scroll-y class="right-aside" @scroll="asideScroll" :scroll-top="tabScrollTop">
			<view v-for="item in slist" :key="item.id" class="s-list" :id="'main-' + item.id">
				<text class="s-item">{{ item.name }}</text>
				<view class="t-list">
					<view class="t-item" v-for="titem in tlist" v-if="titem.category===item.id" @click="navToDetailPage(titem)" :key="titem.id">
						<view class="image-wrapper" :style="{backgroundImage: 'url(' + titem.pic_url + ')'}">
						</view>
						<view class="item-right">
							<text class="title">{{ titem.name }}</text>
							<text class="title"></text>
							<text class="title"></text>
							<text v-if="role==2" class="price">{{titem.purchase_price_register}}</text>
							<text v-if="role==5" class="price">{{titem.purchase_price_corporate}}</text>
							<text v-if="role==0||role==1||role==3||role ==4" class="price">{{titem.retail_price}}</text>

						</view>
					</view>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				sizeCalcState: false,
				tabScrollTop: 0,
				currentId: 1,
				cateList: [],
				role: 0,
				flist: [],
				slist: [],
				tlist: [],
				productList: []
			};
		},
		onLoad() {
			this.loadData();
			console.log("开始加载");
		},
		methods: {
			async loadData() {
				//初始化categories
				this.role = uni.getStorageSync('userDetail').flags;
				this.cateList = await this.getCategories();
				let catelist = this.cateList;
				catelist.forEach(item => {

					if (item.parent === null) {
						this.flist.push(item);
					} else {
						this.slist.push(item);
					}
				});
				//初始化products
				this.productList = await this.getProducts();
				this.productList.forEach(item => {
					this.tlist.push(item);
				});
			},

			//获取以及分类标签
			getCategories: function() {
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "products/categories/",
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


			//获取以及分类标签
			getProducts: function() {
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "products/",
						method: "GET",
						success(res) {
							resolve(res.data)
							console.log(res)
						},
						fail(res) {
							console.log(res)
						}
					})
				}).catch((e) => {});
			},

			//一级分类点击
			tabtap(item) {
				if (!this.sizeCalcState) {
					this.calcSize();
				}
				this.currentId = item.id;
				let index = this.slist.findIndex(sitem => sitem.parent === item.id);
				this.tabScrollTop = this.slist[index].top;
			},
			//右侧栏滚动
			asideScroll(e) {
				if (!this.sizeCalcState) {
					this.calcSize();
				}
				let scrollTop = e.detail.scrollTop;
				let tabs = this.slist.filter(item => item.top <= scrollTop).reverse();
				if (tabs.length > 0) {
					this.currentId = tabs[0].parent;
				}
			},
			//计算右侧栏每个tab的高度等信息
			calcSize() {
				let h = 0;
				this.slist.forEach(item => {
					let view = uni.createSelectorQuery().select('#main-' + item.id);
					view.fields({
							size: true
						},
						data => {
							item.top = h;
							h += data.height;
							item.bottom = h;
						}
					).exec();
				});
				this.sizeCalcState = true;
			},

			//导航至产品详情页面
			navToDetailPage(item) {
				//测试数据没有写id，用title代替
				let id = item.id;
				uni.navigateTo({
					url: `/pages/product/product?id=${id}`
				})
			},
		}
	};
</script>

<style lang="scss">
	page,
	.content {
		height: 100%;
		background-color: #f8f8f8;
	}

	.content {
		display: flex;
	}

	.left-aside {
		flex-shrink: 0;
		width: 200upx;
		height: 100%;
		background-color: #fff;
	}

	.f-item {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100upx;
		font-size: 28upx;
		color: $font-color-base;
		position: relative;

		&.active {
			color: $base-color;
			background: #f8f8f8;

			&:before {
				content: '';
				position: absolute;
				left: 0;
				top: 50%;
				transform: translateY(-50%);
				height: 36upx;
				width: 8upx;
				background-color: $base-color;
				border-radius: 0 4px 4px 0;
				opacity: 0.8;
			}
		}
	}

	.right-aside {
		flex: 1;
		overflow: hidden;
		padding-left: 20upx;
	}

	.s-item {
		display: flex;
		align-items: center;
		height: 70upx;
		padding-top: 8upx;
		font-size: 28upx;
		color: $font-color-dark;
	}

	.t-list {
		display: flex;
		flex-wrap: wrap;
		width: 100%;
		background: #fff;
		padding-top: 12upx;

		&:after {
			content: '';
			flex: 99;
			height: 0;
		}
	}

	.item {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		flex-direction: column;
		width: 176upx;
		font-size: 26upx;
		color: #666;
		padding-bottom: 20upx;

		image {
			width: 140upx;
			height: 140upx;
		}
	}

	.t-item {
		display: flex;
		position: relative;
		padding: 30upx 40upx;

		.image-wrapper {
			width: 180upx;
			height: 180upx;
			flex-shrink: 0;
			position: relative;
			background-size: 100% 100%;


		}

		.item-right {
			display: flex;
			flex-direction: column;
			flex: 1;
			overflow: hidden;
			position: relative;
			padding-left: 30upx;

			.title {
				font-size: $font-base - 6upx;
				color: $font-color-dark;
				height: 40upx;
				line-height: 40upx;

			}

			.price {
				font-size: $font-base - 2upx;
				color: $font-color-dark;
				height: 40upx;
				line-height: 40upx;

				&:before {
					content: '￥';
					font-size: $font-base - 2upx;
					//margin: 0 2upx 0 8upx;
				}
			}

			.attr {
				font-size: $font-sm + 2upx;
				color: $font-color-light;
				height: 50upx;
				line-height: 50upx;
			}

			.price {
				height: 50upx;
				line-height: 50upx;
			}
		}

		.del-btn {
			padding: 4upx 10upx;
			font-size: 34upx;
			height: 50upx;
			color: $font-color-light;
		}
	}
</style>
