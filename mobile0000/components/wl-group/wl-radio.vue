<template>
  <view class="content">
    <radio-group @change="radioChange" :name="name">
      <label :class="item.checked ?  'checkbox selectBox' : 'checkbox '" @click="labelBtn(item.value,index)" v-for="(item,index) in labelList" :key="item.value" >
        <radio :value="item.value" :checked="item.checked" v-show="false"/>{{item.name}}
      </label>
    </radio-group>
  </view>
</template>

<script>
  export default {
		props:{
			labelList: {
				type:[Object,Array],
				default:[{
					name: '单选项',
					value: '0',
					checked: false
				}]
			},
			name:{
				type:String,
				default:'name'
			}
		},
    data() {
      return {
        labelName:'',
        labelDataList:0,
      };
    },
    methods:{
      labelBtn(name,index){
        console.log(name,index,"nameindex")
        this.labelName = name
				for (let i in this.labelList) {
					this.labelList[i].checked = false;
				}
				this.labelList[index].checked = true
      },
      radioChange: function (e) {
        this.labelDataList = e.detail.value
        console.log(e)
        console.log('radio发生change事件，携带value值为：' + e.detail.value)
        console.log(this.labelDataList,"labelDataList")
      },
    }
  }
</script>

<style>
  .selectBox{
    background: #EB5248!important;
    color: #fff!important;
  }
  .checkbox{
    padding: 5px 10px;
    border: 1px solid #EB5248;
    margin: 10px;
    border-radius: 7upx;
    color: #000;
  }
  .content{
    padding: 10px;
  }
</style>
