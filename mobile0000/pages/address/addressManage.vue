<template>
	<view class="content">
		<view class="row b-b">
			<text class="tit">联系人</text>
			<input class="input" type="text" v-model="addressData.contact_name" placeholder="收货人姓名" placeholder-class="placeholder" />
		</view>
		<view class="row b-b">
			<text class="tit">手机号</text>
			<input class="input" type="number" v-model="addressData.contact_phone" placeholder="收货人手机号码" placeholder-class="placeholder" />
		</view>

		<view class="row b-b">
			<text class="tit">所在地区</text>
			<view class='input'>
				<pick-regions :defaultRegion="defaultRegionCode" @getRegion="handleGetRegion">
					<h2 v-if="region==[]">点击选择省市区</h2>
					<h2 v-else>{{regionName}}</h2>
				</pick-regions>
			</view>
		</view>
		<view class="row b-b">
			<text class="tit">详细地址</text>
			<input class="input" type="text" v-model="addressData.address" placeholder="详细地址" placeholder-class="placeholder" />
		</view>
		<view class="row b-b">
			<text class="tit">邮编</text>
			<input class="input" type="text" v-model="addressData.postcode" placeholder="邮编" placeholder-class="placeholder" />
		</view>

		<view class="row default-row">
			<text class="tit">设为默认地址</text>
			<switch :checked="addressData.id == default_address" @change="switchChange" color="#fa436a" />
		</view>

		<view v-if="manageType=='edit'" class="row del-row">
			<text class="txt" @click="deleteAddress(addressData.id)">删除该地址</text>
		</view>
		<button class="add-btn" @click="confirm(addressData.id)">保存</button>
	</view>
</template>

<script>
	import pickRegions from '@/components/pick-regions/pick-regions.vue'
	export default {
		components: {
			pickRegions
		},
		data() {
			return {
				region: [],
				defaultRegion: ['广东省', '广州市', '番禺区'],
				defaultRegionCode: '440113',
				addressData: {
					id: 0,
					contact_name: '',
					contact_phone: '',
					country: '中国',
					province: '',
					city: '',
					address: '',
					postcode: '',
					region: '',
					user: 0
				},
				default_address: 0,
				checked: false,
				manageType: 'edit'
			}
		},
		computed: {
			regionName() {
				return this.region.map(item => item.name).join(' ')
			}
		},
		onLoad(options) {
			let title = '新增收货地址';
			this.addressData.user = uni.getStorageSync("userDetail").id;
			if (options.type == 'edit') {
				title = '编辑收货地址';
				this.addressData = JSON.parse(options.data);
				this.addressData.user = uni.getStorageSync("userDetail").id;
			}
			this.manageType = options.type;
			this.default_address = uni.getStorageSync("userDetail").address_id;
			this.region = [{
				'name': this.addressData.province,
				"code": this.addressData.region[0] + this.addressData.region[1]

			}, {
				"name": this.addressData.city,
				"code": this.addressData.region[0] + this.addressData.region[1] + this.addressData.region[2] + this.addressData.region[
					3]
			}, {
				"name": this.addressData.district,
				"code": this.addressData.region
			}]
			uni.setNavigationBarTitle({
				title
			});

		},
		methods: {
			handleGetRegion(region) {
				this.region = region;
				this.addressData.province = this.region[0].name;
				this.addressData.city = this.region[1].name;
				this.addressData.district = this.region[2].name;
				this.addressData.region = this.region[2].code;

			},
			switchChange(e) {
				this.checked = e.detail.value;
				console.log("switch 开关状态");
				console.log(this.checked);
			},
			//删除该地址
			deleteAddress(id) {
				let that = this;
				uni.showModal({
					title: '提示',
					content: '确定要删除此地址么？',
					success: function(res) {
						that.util
							.request(that.api.ApiRoot + "users/" + uni.getStorageSync("userDetail").id + "/addresses/" + id + "/", {},
								'DELETE', )
							.then(
								uni.navigateBack()
							);
					}
				});
			},
			setDefaultAddress() {},


			//提交  新增地址或者编辑地址
			confirm(id) {
				var data = this.addressData;
				if (!data.contact_name) {
					uni.showModal({
						title: '提示',
						content: '请填写收货人姓名',
						success: function(res) {}
					});
					return;
				}
				if (!/(^1[3|4|5|7|8][0-9]{9}$)/.test(data.contact_phone)) {
					uni.showModal({
						title: '提示',
						content: '请输入正确的手机号码',
						success: function(res) {}
					});
					return;
				}
				let that = this;
				if (that.manageType == "edit") {
					console.log(this.addressData.id);
					let address_id = this.addressData.id;
					let checked = this.checked;

					new Promise(resolve => {
						uni.request({
							header: {
								"content-type": "application/json"
							},
							url: this.api.ApiRoot + "users/" + uni.getStorageSync("userDetail").id + "/addresses/" + this.addressData.id +
								"/",
							data: this.addressData,
							method: "PUT",
							success(res) {
								console.log(res)
								//如果要修改默认地址的话
								//获取userInfo 并用put请求修改

								var userInfo = uni.getStorageSync("userDetail");
								userInfo.address_id = address_id;
								uni.setStorageSync("userDetail", userInfo);

								if (checked == true) {
									uni.request({
										header: {
											"content-type": "application/json"
										},
										url: that.api.ApiRoot + "users/" + uni.getStorageSync("userDetail").id + "/",
										data: {
											"id": uni.getStorageSync("userDetail").id,
											"wx_open_id": uni.getStorageSync("userDetail").wx_open_id,
											"wx_union_id": uni.getStorageSync("userDetail").wx_union_id,
											"wx_name": uni.getStorageSync("userDetail").wx_name,
											"wx_avatar_url": uni.getStorageSync("userDetail").wx_avatar_url,
											"name": uni.getStorageSync("userDetail").name,
											"gender": uni.getStorageSync("userDetail").gender,
											"phone": uni.getStorageSync("userDetail").phone,
											"email": uni.getStorageSync("userDetail").email,
											"address_id": data.id,
											"flags": uni.getStorageSync("userDetail").flags

										},
										method: "PUT",
										success(res) {
											uni.showToast({
												title: "修改默认地址",
												content: "默认地址已修改！"
											})
											uni.navigateBack({});
										},
										fail(res) {
											console.log(res);
											uni.showToast({
												title: "修改默认地址",
												content: "默认地址修改失败！"
											})
											uni.navigateBack({});
										}

									})
								}








								uni.navigateBack({})
							},
							fail(res) {
								console.log(res)
							}
						})
					}).catch((e) => {});
				} else {
					//发送请求
					new Promise(resolve => {
						uni.request({
							header: {
								"content-type": "application/json"
							},
							url: that.api.ApiRoot + "users/" + uni.getStorageSync("userDetail").id + "/addresses/",
							data: data,
							method: "POST",
							success(res) {
								if (res.statusCode == 201) {
									//修改数据库默认地址
									var userInfo = uni.getStorageSync("userDetail");
									userInfo.address_id = res.data.id;
									uni.setStorageSync("userDetail", userInfo);
									uni.request({
										header: {
											"content-type": "application/json"
										},
										url: that.api.ApiRoot + "users/" + uni.getStorageSync("userDetail").id + "/",
										data: {
											"id": uni.getStorageSync("userDetail").id,
											"wx_open_id": uni.getStorageSync("userDetail").wx_open_id,
											"wx_union_id": uni.getStorageSync("userDetail").wx_union_id,
											"wx_name": uni.getStorageSync("userDetail").wx_name,
											"wx_avatar_url": uni.getStorageSync("userDetail").wx_avatar_url,
											"name": uni.getStorageSync("userDetail").name,
											"gender": uni.getStorageSync("userDetail").gender,
											"phone": uni.getStorageSync("userDetail").phone,
											"email": uni.getStorageSync("userDetail").email,
											"address_id": res.data.id,
											"flags": uni.getStorageSync("userDetail").id
										},
										method: "PUT",
										success(res) {
											uni.showToast({
												title: "地址生成",
												content: "地址已经添加！"
											})
											uni.navigateBack({});
										},
										fail(res) {
											console.log(res);
											uni.showToast({
												title: "地址生成",
												content: "地址添加失败！"
											})
											uni.navigateBack({});
										}

									})


								} else {

								}
								uni.navigateBack({})
							},
							fail(res) {
								console.log(res)
							}
						})
					}).catch((e) => {});

					/*这里应该设置默认*/
				}
			},
		}
	}
</script>

<style lang="scss">
	page {
		background: $page-color-base;
		padding-top: 16upx;
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
			width: 120upx;
			font-size: 30upx;
			color: $font-color-dark;
		}

		.input {
			flex: 1;
			font-size: 30upx;
			color: $font-color-dark;
			text-align: right;
		}

		.icon-shouhuodizhi {
			font-size: 36upx;
			color: $font-color-light;
		}
	}

	.default-row {
		margin-top: 16upx;

		.tit {
			flex: 1;
		}

		switch {
			transform: translateX(16upx) scale(.9);
		}
	}

	.del-row {
		margin-top: 16upx;

		.txt {
			display: flex;
			justify-content: center;

			font-size: 30upx;
			color: rgba(170, 0, 0, 102);
		}

	}


	.add-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 690upx;
		height: 80upx;
		margin: 60upx auto;
		font-size: $font-lg;
		color: #fff;
		background-color: $base-color;
		border-radius: 10upx;
		box-shadow: 1px 2px 5px rgba(219, 63, 96, 0.4);
	}
</style>
