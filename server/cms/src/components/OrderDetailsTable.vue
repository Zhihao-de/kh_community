<template>
  <Table
    :data="orderDetails"
    :columns="orderDetailFields"
    :loading="dataLoading"
    stripe
    border
  >
  </Table>
</template>

<script>
/* 导入Order Detail的信息
 */
import { listOrderDetails } from '@/api/order_api'

export default {
  name: 'OrderDetailsTable',
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 商品订单详情列表 */
      orderDetails: [],

      /* 商品订单列表的字段定义 */
      orderDetailFields: [
        {
          type: 'index',
          align: 'center',
          width: 60,
          resizable: true
        },
        {
          title: '商品名称',
          minWidth: 300,
          resizable: true,
          render: (h, params) => {
            return h('span', params.row.product.name)
          }
        },
        {
          title: '重量',
          align: 'center',
          width: 120,
          resizable: true,
          render: (h, params) => {
            return h(
              'span',
              params.row.product.weight + params.row.product.unit
            )
          }
        },
        {
          title: '数量(件)',
          key: 'quantity',
          align: 'center',
          width: 90,
          resizable: true
        },
        {
          title: '交易价(元)',
          key: 'purchase_price',
          align: 'center',
          width: 130,
          resizable: true
        },
        {
          title: '总价(元)',
          key: 'total_price',
          align: 'center',
          width: 90,
          resizable: true
        }
      ]
    }
  },
  created () {
    console.log('输出上页传来的数据')
    console.log(this.$route.params.order)
    this.getOrderDetails(this.$route.params.order.id)
  },
  methods: {
    /**
     * 获取商品订单明细
     * @param {Object} orderId 商品订单ID
     */
    getOrderDetails (orderId) {
      this.dataLoading = true
      listOrderDetails(orderId)
        .then(res => {
          this.orderDetails = res.data
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err)
          this.dataLoading = false
        })
    }
  }
}
</script>

<style scoped>
.model-viewer-description-center {
  display: block;
  width: 800px;
  margin: 0 auto;
  overflow: auto;
}
</style>
