<template>
  <div>
    <Table
      :data="orders"
      :columns="orderFields"
      :loading="dataLoading"
      stripe
      border
    >
    </Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <Page
          :page-size="4"
          :total="count"
          :current="1"
          @on-change="onPageChanged"
        ></Page>
      </div>
    </div>
  </div>
</template>

<script>
import {
  listOrders,
  getOrderFlagsText,
  getOrderFlagsColor,
  patchOrderByFlags
} from '@/api/order_api'

export default {
  name: 'OrdersTable',
  components: {},
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 产品总数，用于设置分页器 */
      count: 0,

      /* 产品模型列表 */
      orders: [],

      /* 产品列表的字段定义 */
      orderFields: [
        {
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
        },
        {
          title: '退款原因',
          key: 'refund_reason',
          align: 'center',
          width: 120,
          resizable: true
        },
        {
          title: '操作',
          fixed: 'right',
          align: 'center',
          width: 160,
          resizable: true,
          render: (h, params) => {
            var children = [
              h(
                'Button',
                {
                  props: {
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    // click事件进行跳转
                    click: () => {
                      this.$router.push({
                        name: 'order_view',
                        params: { order: params.row }
                      })
                    }
                  }
                },
                '详情'
              )
            ]
            if (params.row.flags === 1 /* 已付款 */) {
              children.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.$router.push({
                          name: 'order_view',
                          params: { order: params.row }
                        })
                      }
                    }
                  },
                  '配送'
                )
              )
            } else if (params.row.flags === 5 /* 已付款 */) {
              children.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'error',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.$router.push({
                          name: 'order_refund',
                          params: { order: params.row }
                        })
                      }
                    }
                  },
                  '退款'
                )
              )
            }
            return h('div', children)
          }
        }
      ]
    }
  },
  created () {
    this.getOrders(1)
  },
  methods: {
    /**
     * 获取商品订单列表
     * @param {Object} page 页索引
     */
    getOrders (page) {
      this.dataLoading = true
      listOrders(page)
        .then(res => {
          this.orders = res.data.results
          this.count = res.data.count
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err)
          this.dataLoading = false
        })
    },
    /**
     * 更新商品订单状态
     * @param currentOrder 当前商品订单对象
     * @param flags 订单状态
     * @returns {*}
     */
    updateOrderByFlags (currentOrder, flags) {
      const oldFlagsColor = this.getFlagsColor(currentOrder.flags)
      const newFlagsColor = this.getFlagsColor(flags)
      this.$Modal.confirm({
        title: '操作确认',
        content:
          '确定将产品订单 <strong>' +
          currentOrder.id +
          "</strong> 的状态从 <font color='" +
          oldFlagsColor +
          "'>" +
          this.getFlagsText(currentOrder.flags) +
          "</font> 转变为 <font color='" +
          newFlagsColor +
          "'>" +
          this.getFlagsText(flags) +
          '</font> ？',
        onOk: () => {
          this.dataLoading = true
          patchOrderByFlags(currentOrder.id, flags)
            .then(() => {
              currentOrder.flags = flags
              this.$Message.info('操作成功！')
              this.dataLoading = false
            })
            .catch(err => {
              this.$Message.error(err)
              this.dataLoading = false
            })
        }
      })
    },
    /**
     * 换页的事件处理
     * @param page 页索引
     * @returns {*}
     */
    onPageChanged (page) {
      this.getOrders(page)
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
