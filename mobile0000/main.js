import Vue from 'vue'
import store from './store'
import App from './App'
import TMap from './config/qqmap-wx-jssdk.min.js'

const msg = (title, duration = 1500, mask = false, icon = 'none') => {
	//统一提示方便全局修改
	if (Boolean(title) === false) {
		return;
	}
	uni.showToast({
		title,
		duration,
		mask,
		icon
	});
}

const prePage = () => {
	let pages = getCurrentPages();
	let prePage = pages[pages.length - 2];
	// #ifdef H5
	return prePage;
	// #endif
	return prePage.$vm;
}


Vue.config.productionTip = false
Vue.prototype.util = require('utils/utils.js');
Vue.prototype.api = require('config/api.js');

//引入腾讯地图
//const tMap = new this.Tmap({
//	key: 'MQCBZ-PPLCD-E6R4G-PPXQS-FJCHV-B7BOP'
//})


//全局参数
import gdata from './config/globalCommon.js'
Vue.prototype.$gdata = gdata;


App.mpType = 'app'

const app = new Vue({
	...App
})
app.$mount()
