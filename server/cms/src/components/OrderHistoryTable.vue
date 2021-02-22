<template>
  <div>
    <Table :data="orderHistory" :columns="orderHistoryFields" :loading="dataLoading" stripe border>
    </Table>
  </div>
</template>

<script>
import {
  listOrderHistory,
  defaultOrderHistory,
  getOrderFlagsText,
  getOrderFlagsColor
} from '@/api/order_api'

export default {
  name: 'OrderHistoryTable',
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,
      historyInfo: '',
      currentOrderHistory: defaultOrderHistory(),

      /* 商品订单物流详情列表 */
      orderHistory: [],

      /* 产品物流列表的字段定义 */
      orderHistoryFields: [{
        type: 'index',
        align: 'center',
        width: 60,
        resizable: true
      },
      {
        title: '状态',
        key: 'flags',
        align: 'center',
        width: 130,
        sortable: true,
        resizable: true,
        render: (h, params) => {
          return h(
            'Tag', {
              props: {
                type: 'dot',
                color: getOrderFlagsColor(params.row.flags)
              }
            },
            getOrderFlagsText(params.row.flags)
          )
        }
      },
      {
        title: '订单号',
        key: 'serial_number',
        align: 'center',
        width: 210,
        resizable: true
      },
      {
        title: '用户微信',
        minWidth: 240,
        resizable: true,
        render: (h, params) => {
          const wx_name = params.row.user.wx_name
          const wx_mobile = params.row.user.mobile
          const wx_avatar_url = params.row.user.wx_avatar_url
          return h(
            'div', {
              style: {
                marginTop: '8px'
              }
            },
            [
              h(
                'div', {
                  style: {
                    float: 'left'
                  }
                },
                [
                  h('img', {
                    attrs: {
                      src: wx_avatar_url
                    },
                    style: {
                      width: '48px',
                      height: '48px',
                      marginRight: '16px'
                    }
                  })
                ]
              ),
              h('div', [h('div', wx_name), h('div', wx_mobile)])
            ]
          )
        }
      },
      {
        title: '用户姓名',
        align: 'center',
        width: 120,
        resizable: true,
        render: (h, params) => {
          return h('span', params.row.order.name)
        }
      },
      {
        title: '联系电话',
        align: 'center',
        width: 150,
        resizable: true,
        render: (h, params) => {
          return h('span', params.row.order.phone)
        }
      },

      {
        title: '总金额(元)',
        key: 'list_amount',
        width: 110,
        resizable: true
      },

      {
        title: '下单时间',
        key: 'created_at',
        align: 'center',
        width: 120,
        resizable: true
      },
      {
        title: '更新时间',
        key: 'updated_at',
        align: 'center',
        width: 120,
        resizable: true
      },
      {
        title: '退款',
        key: 'refund',
        align: 'center',
        width: 120,
        resizable: true
      },
      {
        title: '退款原因',
        key: 'refund_reason',
        align: 'center',
        width: 120,
        resizable: true
      }
      ]
    }
  },
  created () {
    this.getOrderHistory(this.$route.params.order.id)
  },

  methods: {
    /**
       * 获取商品订单历史记录
       * @param {Object} orderId 商品订单ID
       */
    getOrderHistory (orderId) {
      this.dataLoading = true
      listOrderHistory(orderId)
        .then(res => {
          console.log(res.data)
          this.orderHistory = res.data
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
