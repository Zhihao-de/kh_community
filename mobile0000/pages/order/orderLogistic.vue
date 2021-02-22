<template>
	<view>
		<view class="content">
			<logistics :wlInfo="wlInfo" :address = "address"></logistics>

		</view>

	</view>
</template>

<script>
	import logistics from '@/components/xinyu-logistics/xinyu-logistics.vue';

	export default {
		components: {
			logistics
		},

		data() {
			return {
				address:{
					"country":"中国",
					"province":"北京市",
					"city":"北京市",
					"address":"回龙观1区"
				},
				wlInfo: {
					"number": "YT3142350917528",
					"type": "yto",
					"list": [{
							"time": "2020-12-27 15:28:15",
							"status": "客户签收人: 本人签收 已签收  感谢使用圆通速递，期待再次为您服务 如有疑问请联系：18947661743，投诉电话：010-53576707。疫情期间圆通每天对网点多次消毒，快递小哥每天测量体温，佩戴口罩"
						},
						{
							"time": "2020-12-27 11:44:43",
							"status": "北门沫森护肤造型妈妈驿站妈妈驿站已发出自提短信,请上门自提,联系电话15321889392"
						},
						{
							"time": "2020-12-27 11:44:42",
							"status": "快件已到达北门沫森护肤造型妈妈驿站妈妈驿站,联系电话15321889392"
						},
						{
							"time": "2020-12-27 11:43:00",
							"status": "【北京市昌平区新龙城公司】 派件中  派件人: 王国为 电话 18947661743 。 圆通快递小哥每天已测体温，请放心收寄快递 如有疑问，请联系：010-53576707"
						},
						{
							"time": "2020-12-26 18:23:23",
							"status": "【华北转运中心】 已发出 下一站 【北京市昌平区新龙城公司】"
						},
						{
							"time": "2020-12-26 18:03:13",
							"status": "【华北转运中心公司】 已收入"
						},
						{
							"time": "2020-12-25 22:14:42",
							"status": "【上海转运中心】 已发出 下一站 【华北转运中心公司】"
						},
						{
							"time": "2020-12-25 22:12:26",
							"status": "【上海转运中心公司】 已收入"
						},
						{
							"time": "2020-12-25 20:53:28",
							"status": "【上海市青浦区徐泾】 已发出 下一站 【上海转运中心公司】"
						},
						{
							"time": "2020-12-25 20:47:35",
							"status": "【上海市青浦区徐泾公司】 已打包"
						},
						{
							"time": "2020-12-25 20:43:48",
							"status": "【上海市青浦区徐泾公司】 已收件 取件人: 滕金龙 (18702112423)"
						}
					],
					"deliverystatus": "3",
					"issign": "1",
					"expName": "圆通速递",
					"expSite": "www.yto.net.cn ",
					"expPhone": "95554",
					"logo": "https://img3.fegine.com/express/yto.jpg",
					"courier": "",
					"courierPhone": "18947661743",
					"updateTime": "2020-12-27 15:28:15",
					"takeTime": "1天18小时44分"
				}

			}
		},
		methods: {

		}
	}
</script>

<style>

</style>
