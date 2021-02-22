/**
 * 封装request
 */

function request(url, data = {}, method = "", header) {
	return new Promise(function(reslove, reject) {
		uni.showLoading({
			title: '加载中...'
		});
		uni.request({
			url: url, //仅为示例，并非真实接口地址。
			data: data,
			method: method,
			header: header,
			success: (res) => {
				//先判断是否为登录信息
				if ("errno" in res) {
					if (res.errno == 0) {
						uni.hideLoading()
						if (res.data.errno == 501) {
							uni.redirectTo({
								url: '/pages/public/login'
							});
						} else {
							reslove(res.data) //状态由等待变为成功，传的参数作为then函数中成功函数的实参
						}

					} else {
						uni.hideLoading()
						reject('请求失败') //状态由等待变为失败，传的参数作为then函数中失败函数的实参
					}

				} else {
					uni.hideLoading()
					reslove(res.data)
				}

			},
			fail: function(err) {
				uni.hideLoading()
				reject(err)
			}
		});
		//reslove('成功')  //状态由等待变为成功，传的参数作为then函数中成功函数的实参
	})
}

/**
 * 上传图片
 */
function upFileRequest(url) {
	return new Promise(function(reslove, reject) {
		uni.chooseImage({
			count: 1, //默认9
			sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
			sourceType: ['album'], //从相册选择
			success: function(res) {
				const tempFilePaths = res.tempFilePaths;
				uni.uploadFile({
					url: url, //仅为示例，非真实的接口地址
					filePath: tempFilePaths[0],
					name: 'file',
					header: {
						'Content-Type': 'application/json', //自定义请求头信息
						'Authorization': 'ZJSS ' + uni.getStorageSync('token')
					},
					success: (uploadFileRes) => {
						var obj_group = JSON.stringify(uploadFileRes.data);
						if (uploadFileRes.statusCode == 200) {
							if (obj_group.errno == 501) {
								try {
									uni.removeStorageSync('token');
									uni.removeStorageSync('userInfo');
								} catch (e) {
									// error
								}
								//跳转登录页  pages/public/login
								uni.navigateTo({
									url: '/pages/public/login'
								});
							} else {
								reslove(obj_group.data.url) //状态由等待变为成功，传的参数作为then函数中成功函数的实参
							}
						} else {
							reject('请求失败') //状态由等待变为失败，传的参数作为then函数中失败函数的实参
						}
					},
					fail: function(err) {
						reject(err)
					},
				});
			},
			fail: function(error) {
				reject(error)
			}
		});
	})
}


function formatLocation(longitude, latitude) {
	if (typeof longitude === 'string' && typeof latitude === 'string') {
		longitude = parseFloat(longitude)
		latitude = parseFloat(latitude)
	}

	longitude = longitude.toFixed(2)
	latitude = latitude.toFixed(2)

	return {
		longitude: longitude.toString().split('.'),
		latitude: latitude.toString().split('.')
	}
}
module.exports = {
	request,
	upFileRequest,
	formatLocation
}
