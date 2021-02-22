<template>
  <div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>订单信息</strong></p>
        <Button slot="extra" icon="md-refresh" @click="refreshOrder"></Button>
        <Table
          :data="orders"
          :columns="orderFields"
          :loading="dataLoading"
          stripe
          border
        >
        </Table>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>支付信息</strong></p>
        <Button
          slot="extra"
          icon="md-refresh"
          @click="refreshTransaction"
        ></Button>
        <OrderTransactionsTable
          @on-update="handleOrderTransactionUpdate"
        ></OrderTransactionsTable>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>商品清单</strong></p>
        <OrderDetailsTable></OrderDetailsTable>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>物流信息</strong></p>
        <OrderRoutesTable
          @on-update="handleOrderRouteUpdate"
        ></OrderRoutesTable>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>历史记录</strong></p>
        <OrderHistoryTable
          @on-update="handleOrderHistoryUpdate"
        ></OrderHistoryTable>
      </Card>
    </div>
  </div>
</template>

<script>
import {
  ORDER_FLAGS,
  getOrder,
  getOrderFlagsText,
  getOrderFlagsColor,
  patchOrderByFlags
} from '@/api/order_api'
import OrderTransactionsTable from '@/components/OrderTransactionsTable'
import OrderDetailsTable from '@/components/OrderDetailsTable'
import OrderRoutesTable from '@/components/OrderRoutesTable'
import OrderHistoryTable from '@/components/OrderHistoryTable'

export default {
  name: 'OrderDetailView.vue',
  components: {
    OrderTransactionsTable,
    OrderDetailsTable,
    OrderRoutesTable,
    OrderHistoryTable
  },
  data () {
    return {
      dataLoading: false,

      orderId: this.$route.params.order.id,

      /* 订单列表（就一项） */
      orders: [this.$route.params.order],

      /* 商品列表的字段定义 */
      orderFields: [
        {
          title: '状态',
          key: 'flags',
          align: 'center',
          width: 130,
          sortable: true,
          resizable: true,
          render: (h, params) => {
            return h(
              'Tag',
              {
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
              'div',
              {
                style: {
                  marginTop: '8px'
                }
              },
              [
                h(
                  'div',
                  {
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
            return h('span', params.row.name)
          }
        },
        {
          title: '联系电话',
          align: 'center',
          width: 150,
          resizable: true,
          render: (h, params) => {
            return h('span', params.row.phone)
          }
        },
        {
          title: '收货地址',
          minWidth: 200,
          resizable: true,
          render: (h, params) => {
            const r = params.row
            return h(
              'span',
              r.country +
                ',' +
                r.province +
                ',' +
                r.city +
                ',' +
                r.address +
                ',' +
                r.postcode
            )
          }
        },
        {
          title: '总金额(元)',
          key: 'amount',
          width: 110,
          resizable: true
        },
        {
          title: '商品数量',
          key: 'quantity',
          align: 'center',
          width: 100,
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
        }
      ]
    }
  },
  methods: {
    getOrderById (orderId) {
      this.dataLoading = true
      getOrder(orderId)
        .then(res => {
          this.$route.params.order = res.data
          this.orders = [res.data]
          this.dataLoading = false
        })
        .catch(err => {
          this.dataLoading = false
          this.$Message.error(err.toString())
        })
    },
    handleOrderRouteUpdate () {
      patchOrderByFlags(this.orderId, ORDER_FLAGS.DELIVERED)
        .then(() => {
          this.$route.params.order.flags = ORDER_FLAGS.DELIVERED
        })
        .catch(err => {
          this.$Message.error(err)
        })
    },
    handleOrderTransactionUpdate () {
      patchOrderByFlags(this.orderId, ORDER_FLAGS.REFUNDED)
        .then(() => {
          this.$route.params.order.flags = ORDER_FLAGS.REFUNDED
        })
        .catch(err => {
          this.$Message.error(err)
        })
    },
    handleOrderHistoryUpdate () {
      patchOrderByFlags(this.orderId, ORDER_FLAGS.REFUNDED)
        .then(() => {
          this.$route.params.order.flags = ORDER_FLAGS.REFUNDED
        })
        .catch(err => {
          this.$Message.error(err)
        })
    },

    refreshOrder () {
      if (this.dataLoading) {
        this.$Message.error('请勿频繁刷新！')
        return
      }
      this.getOrderById(this.orderId)
    },
    refreshTransaction () {}
  }
}
</script>

<style scoped></style>
