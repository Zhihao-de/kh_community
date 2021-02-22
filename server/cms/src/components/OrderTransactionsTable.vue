<template>
  <div>
    <Table
      :data="orderTransactions"
      :columns="orderTransactionFields"
      :loading="dataLoading"
      stripe
      border
    >
    </Table>
  </div>
</template>

<script>
import {
  ORDER_FLAGS,
  listOrderTranscations,
  getPaymentMethodText
  // patchOrderTransactionByRefund
} from '@/api/order_api'

export default {
  name: 'OrderTransactionsTable',
  components: {},
  data () {
    return {
      dataLoading: false,
      orderTransactions: [],
      orderTransactionFields: [
        {
          type: 'index',
          align: 'center',
          width: 60,
          resizable: true
        },
        {
          title: '创建时间',
          key: 'created_at',
          align: 'center',
          width: 120,
          resizable: true
        },
        {
          title: '支付方式',
          align: 'center',
          width: 130,
          resizable: true,
          render: (h, params) => {
            return h('span', getPaymentMethodText(params.row.payment_method))
          }
        },
        {
          title: '支付金额(元)',
          key: 'amount',
          width: 140,
          resizable: true
        },
        {
          title: '交易ID',
          key: 'transaction_id',
          minWidth: 200,
          resizable: true
        },
        {
          title: '交易状态',
          key: 'status',
          width: 110,
          resizable: true
        },
        {
          title: '付款时间',
          key: 'paid_at',
          align: 'center',
          width: 120,
          resizable: true
        },
        {
          title: '退款金额(元)',
          key: 'refund',
          width: 120,
          resizable: true
        },
        {
          title: '退款时间',
          key: 'refunded_at',
          align: 'center',
          width: 120,
          resizable: true
        },
        {
          title: '操作',
          fixed: 'right',
          align: 'center',
          width: 140,
          resizable: true,
          render: (h, params) => {
            if (this.$route.params.order.flags !== ORDER_FLAGS.REFUNDED) {
              return h(
                'Button',
                {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.refund(params.row)
                    }
                  }
                },
                '退款'
              )
            }
          }
        }
      ]
    }
  },
  created () {
    this.getOrderTransactions(this.$route.params.order.id)
  },
  methods: {
    /**
     * 获取商品订单交易记录
     * @param {Object} orderId 商品订单ID
     */
    getOrderTransactions (orderId) {
      this.dataLoading = true
      listOrderTranscations(orderId)
        .then(res => {
          this.orderTransactions = res.data
          this.count = res.data.count
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err)
          this.dataLoading = false
        })
    },
    /**
     * 退款
     * @param currentTransaction 当前商品订单交易对象
     * @returns {*}
     */
    refund (currentTransaction) {
      this.$Modal.confirm({
        title: '操作确认',
        content:
          '确定向用户 <strong>' +
          this.$route.params.order.wx_name +
          "</strong> <font color='red'>退款</font> 金额 <font color='green'>" +
          currentTransaction.amount +
          '</font> 元？',
        onOk: () => {
          // patchOrderTransactionByRefund(currentTransaction)
          //   .then(() => {})
          //   .catch(err => {
          //     this.$Message.error(err.toString());
          //   });
          this.$Message.info('建设中...')
          this.$emit('on-update')
        }
      })
    }
  }
}
</script>

<style></style>
