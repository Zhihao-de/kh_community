<template>
  <div>
    <Form label-position="left" :label-width="60" :model="location" :rules="ruleValidate" inline>
      <FormItem label="地址" prop="address">
        <Input v-model="location.address" placeholder="请输入地址..." style="width: 300px" />
      </FormItem>
      <FormItem>
        <Button type="primary" style="margin-right: 10px" @click="locate">定位</Button>
        <Button type="primary" @click="confirmSubmit">提交</Button>
      </FormItem>
    </Form>
    <div id="map"></div>
  </div>
</template>

<script>
import {
  TMAP_KEY,
  getTMap,
  getUserLocation,
  postUserLocation
} from '@/api/user_api'

export default {
  name: 'UserLocationEditor',
  data () {
    return {
      map: null,
      mapMarker: null,
      infoWindow: null,
      location: {
        user: this.$route.params.user.id,
        address: '',
        lat: 0.0,
        lng: 0.0
      },
      ruleValidate: {
        address: [{
          required: true,
          message: '地址不能为空',
          trigger: 'blur'
        }]
      }
    }
  },
  mounted () {
    getTMap().then(TMap => {
      var center = new TMap.LatLng(39.916527, 116.397128)
      this.map = new TMap.Map(document.getElementById('map'), {
        center: center, // 设置地图中心点坐标
        zoom: 13 // 设置地图缩放级别
      })

      const userId = this.$route.params.user.id
      getUserLocation(userId)
        .then(res => {
          if (res.data.length > 0) {
            this.location = res.data[0]
            center = new TMap.LatLng(this.location.lat, this.location.lng)
          }
          this.map.setCenter(center)
          this.setMarker(center)
          this.setInfoWindow(center)
        })
        .catch(err => {
          this.$Message.error(err.toString())
        })
    })
  },
  created () {},
  methods: {
    locate () {
      if (!this.location.address) {
        return
      }
      this.$jsonp(
        'https://apis.map.qq.com/ws/geocoder/v1/?address=' +
            this.location.address +
            '&key=' +
            TMAP_KEY +
            '&output=jsonp'
      )
        .then(res => {
          if (res.status === 0) {
            const lng = res.result.location.lng
            const lat = res.result.location.lat
            const position = new window.TMap.LatLng(lat, lng)
            this.map.setCenter(position)
            this.setMarker(position)
            this.setInfoWindow(position)
          } else {
            console.log(res.message)
            this.$Message.error(res.message)
          }
          // let address = json.result.address;
          // console.log(address); //附近街道地址信息
        })
        .catch(err => {
          console.log(err)
          this.$Message.error(err.toString())
        })
    },
    confirmSubmit () {
      this.$Modal.confirm({
        title: '操作确认',
        content: '确定提交用户地理位置？',
        onOk: () => {
          this.submit()
        },
        onCancel: () => {}
      })
    },
    submit () {
      postUserLocation(this.location)
        .then(res => {
          console.log(res)
          this.$Message.info('操作成功！')
        })
        .catch(err => {
          console.log(err)
          this.$Message.error(err.toString())
        })
    },
    setMarker (position) {
      const geometry = {
        id: 'user_loc',
        styleId: 'marker',
        position: position,
        properties: {
          title: 'marker'
        }
      }
      if (this.mapMarker) {
        this.mapMarker.setGeometries([geometry])
      } else {
        this.mapMarker = new window.TMap.MultiMarker({
          id: 'marker-layer',
          map: this.map,
          styles: {
            marker: new window.TMap.MarkerStyle({
              width: 23,
              height: 35,
              anchor: {
                x: 12,
                y: 32
              }
            })
          },
          geometries: [geometry]
        })
        // 监听标注点击事件
        const that = this
        this.mapMarker.on('click', function (evt) {
          that.setInfoWindow(evt.geometry.position)
        })
      }
    },
    setInfoWindow (position) {
      // 初始化infoWindow
      const content =
          "<div style='margin-top: 4px; width: 180px; height: 70px'>\
		  <div style='float: left'>\
		    <img\
		      width='64'\
		      height='64'\
		      style='margin-right: 16px'\
		      src='" +
          this.$route.params.user.wx_avatar_url +
          "'\
		    />\
		  </div>\
		  <div>\
		    <h3>" +
          this.$route.params.user.wx_name +
          "</h3>\
		    <div style='color: dimgrey'>" +
          this.$route.params.user.phone +
          '</div>\
		  </div>\
		</div>'
      if (this.infoWindow) {
        this.infoWindow.close()
        this.infoWindow.setPosition(position)
        this.infoWindow.setContent(content)
      } else {
        this.infoWindow = new window.TMap.InfoWindow({
          map: this.map,
          position: position,
          offset: {
            x: 0,
            y: -32
          },
          content: content
        })
      }
      this.infoWindow.open()
    }
  }
}
</script>

<style>
  #map {
    /*地图(容器)显示大小*/
    width: 100%;
    height: 600px;
  }
</style>
