<template>
	<view class="content">
		<map class="map" id="map1" ref="map1" :controls="controls" :longitude="location.longitude" :latitude="location.latitude"
		 :show-location="showLocation" :show-compass="showCompass" :enable-overlooking="enableOverlooking" :enable-zoom="enableZoom"
		 :enable-scroll="enableScroll" :enable-rotate="enableRotate" :enable-traffic="enableTraffic" :markers="markers"
		 :include-points="includePoints" @controltap="oncontroltap" @makertap='makertap'>
		</map>
	</view>
</template>

<script>
	var util = require('@/common/util.js');
	var formatLocation = util.formatLocation;
	// #ifdef APP-PLUS
	import permision from "@/common/permission.js"
	// #endif

	export default {
		data() {
			return {
				id: 0,
				users: [],
				pos_id: 0,
				positions: [],
				hasLocation: false,
				location: {
					latitude: 39.908692,
					longitude: 116.397477
				},
				controls: [{
					id: 1,
					position: {
						left: 5,
						top: 180,
						width: 30,
						height: 30
					},
					iconPath: '/static/logo.png',
					clickable: true
				}],
				includePoints: [],
				showLocation: true,
				scale:13,
				showCompass: true,
				enableZoom: true,
				enableScroll: true,
				enableRotate: true,
				enableSatellite: false,
				enableTraffic: false,
				markers: [],
				includePoints: [],
				rotate: 0,




			}
		},
		onLoad() {
			this.loadData();

			//this.getLocation();

		},
		onReady() {
			this.map = uni.createMapContext("map1", this);
		},
		methods: {

			changeShowCompass(e) {
				this.showCompass = e.detail.value;
			},
			changeEnableOverlooking(e) {
				this.enableOverlooking = e.detail.value;
			},
			changeEnableZoom(e) {
				this.enableZoom = e.detail.value;
			},
			changeEnableScroll(e) {
				this.enableScroll = e.detail.value;
			},
			changeEnableRotate(e) {
				this.enableRotate = e.detail.value;
			},
			changeEnableTraffic(e) {
				this.enableTraffic = e.detail.value;
			},
			getCenterLocation() {
				this.map.getCenterLocation({
					success: ret => {
						//console.log(JSON.stringify(ret));
					}
				})
			},

			async loadData() {
				this.id = uni.getStorageSync("userDetail").id;
				var userlist = await this.getUsers();
				this.users = userlist;
				var locationList = await this.getPositions();
				for (var x in locationList) {
					if (locationList[x].user == this.id) {
						console.log(locationList[x]);
						this.location.longitude = locationList[x].lng;
						this.location.latitude = locationList[x].lat;
						this.pos_id = locationList[x].id;
						console.log("我的地址ID是" + this.pos_id);
					}
				}
				this.positions = locationList;
				this.transferPositionToMarker();
				this.getLocation(this.pos_id);

			},
			//获取所有的用户信息
			getUsers() {
				let that = this;
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "users/",

						method: "GET",
						success(res) {
							resolve(res.data);
						},
						fail(res) {
							console.log(res);
						}
					})
				}).catch((e) => {});
			},
			//获取所有用户的位置信息
			getPositions() {
				let that = this;
				//这里要先更新再
				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "locations/",

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
			//坐标准换为markers
			transferPositionToMarker() {
				var pos = this.positions;
				var marks = [];
				var includePoints = [];
				for (var i in pos) {
					console.log(pos[i]);
					includePoints[i] = {
						latitude: pos[i].lat,
						longitude: pos[i].lng,
					};
					marks[i] = {
						id: pos[i].id,
						latitude: pos[i].lat,
						longitude: pos[i].lng,
						iconPath: '/static/p.svg',
						callout: {
							content: 
								this.users[i].wx_name +'/n'+
								this.users[i].phone,
							borderRadius: 10,
							padding: 5,
							display: 'BYCLICK'
						}
					}
				}
				this.markers = marks;
				this.includePoints = includePoints;

			},

			async getLocation(pos_id) {
				// #ifdef APP-PLUS
				let status = await this.checkPermission();
				if (status !== 1) {
					return;
				}
				// #endif
				// #ifdef MP-WEIXIN 
				var status = await this.getSetting();
				if (status === 2) {
					this.showConfirm();
					return;
				}
				// #endif
				this.doGetLocation(pos_id);
			},
			doGetLocation(pos_id) {
				uni.getLocation({
					success: (res) => {

						var location = {
							latitude: res.latitude,
							longitude: res.longitude
						};
						console.log(location.latitude)
						console.log(location.latitude)
						console.log(uni.getStorageSync('userDetail').id)

						new Promise(resolve => {
							uni.request({
								header: {
									"content-type": "application/JSON"
								},
								url: this.api.ApiRoot + "locations/" + pos_id + "/",
								data: {
									"id": this.pos_id,
									"address": "当前地址",
									"lat": location.latitude,
									"lng": location.longitude,
									"user": uni.getStorageSync('userDetail').id
								},

								method: "PUT",
								success(res) {
									console.log("位置更新成功");
									console.log(res)
								},
								fail(res) {
									console.log(res)
								}
							})
						}).catch((e) => {});


					},
					fail: (err) => {
						// #ifdef MP-BAIDU
						if (err.errCode === 202 || err.errCode === 10003) { // 202模拟器 10003真机 user deny
							this.showConfirm();
						}
						// #endif
						// #ifndef MP-BAIDU
						if (err.errMsg.indexOf("auth deny") >= 0) {
							uni.showToast({
								title: "访问位置被拒绝"
							})
						} else {
							uni.showToast({
								title: err.errMsg
							})
						}
						// #endif
					}
				})
			},

			getSetting: function() {
				return new Promise((resolve, reject) => {
					uni.getSetting({
						success: (res) => {
							if (res.authSetting['scope.userLocation'] === undefined) {
								resolve(0);
								return;
							}
							if (res.authSetting['scope.userLocation']) {
								resolve(1);
							} else {
								resolve(2);
							}
						}
					});
				});
			},
			openSetting: function() {
				this.hideConfirm();
				uni.openSetting({
					success: (res) => {
						if (res.authSetting && res.authSetting['scope.userLocation']) {
							this.doGetLocation();
						}
					},
					fail: (err) => {}
				})
			},
			async checkPermission() {
				let status = permision.isIOS ? await permision.requestIOS('location') :
					await permision.requestAndroid('android.permission.ACCESS_FINE_LOCATION');
				if (status === null || status === 1) {
					status = 1;
				} else if (status === 2) {
					uni.showModal({
						content: "系统定位已关闭",
						confirmText: "确定",
						showCancel: false,
						success: function(res) {}
					})
				} else if (status.code) {
					uni.showModal({
						content: status.message
					})
				} else {
					uni.showModal({
						content: "需要定位权限",
						confirmText: "设置",
						success: function(res) {
							if (res.confirm) {
								permision.gotoAppSetting();
							}
						}
					})
				}
				return status;
			},
			clear: function() {
				this.hasLocation = false
			},
			// 点击marker
			makertap(e) {
				uni.showModal({
					content: JSON.stringify(e)
				});
			}


		}
	}
</script>

<style>
	.content {
		flex: 1;

	}

	.map {
		width: 750rpx;
		height: 1500rpx;


		background-color: #f0f0f0;
	}

	.scrollview {
		flex: 1;
		padding: 10px;
	}

	.list-item {
		flex-direction: row;
		flex-wrap: nowrap;
		align-items: center;
		padding: 5px 0px;
	}

	.list-text {
		flex: 1;
	}

	.button {
		margin-top: 5px;
		margin-bottom: 5px;
	}

	.tips {
		width: 600rpx;
		height: 100rpx;
		margin: 10rpx auto;
		border-radius: 10rpx;
		position: absolute;
		top: 10rpx;
		left: 50%;
		transform: translate(-50%, 0);
		z-index: 2;
		overflow: hidden;
	}
</style>
