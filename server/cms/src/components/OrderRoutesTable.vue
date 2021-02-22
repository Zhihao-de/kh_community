<template>
  <div>
    <Button
      type="primary"
      style="margin-bottom: 16px"
      @click="openOrderRouteEditor"
      >新增物流</Button
    >
    <Table
      :data="orderRoutes"
      :columns="orderRouteFields"
      :loading="dataLoading"
      stripe
      border
    >
    </Table>
    <Modal title="查看物流信息" v-model="showRouteInfo" :footer-hide="true">
      <div v-if="showRouteInfo" style="width: 100%" v-html="routeInfo" />
    </Modal>
    <Modal
      title="编辑物流信息"
      v-model="showRouteEditor"
      :footer-hide="true"
      :width="800"
    >
      <OrderRouteEditor
        :model="currentOrderRoute"
        v-if="showRouteEditor"
        @on-update="handleOrderRouteUpdate"
      ></OrderRouteEditor>
    </Modal>
  </div>
</template>

<script>
import { listOrderRoutes, defaultOrderRoute } from '@/api/order_api'
import OrderRouteEditor from '@/components/OrderRouteEditor'

export default {
  name: 'OrderRoutesTable',
  components: {
    OrderRouteEditor
  },
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      showRouteInfo: false,

      routeInfo: '',

      showRouteEditor: false,

      currentOrderRoute: defaultOrderRoute(),

      /* 商品订单物流详情列表 */
      orderRoutes: [],

      /* 产品物流列表的字段定义 */
      orderRouteFields: [
        {
          type: 'index',
          align: 'center',
          width: 60,
          resizable: true
        },
        {
          title: '物流公司',
          key: 'express',
          align: 'center',
          width: 100,
          resizable: true
        },
        {
          title: '物流单号',
          key: 'receipt_no',
          align: 'center',
          width: 200,
          resizable: true
        },
        {
          title: '收件人信息',
          key: 'address',
          minWidth: 300,
          resizable: true
        },
        {
          title: '数量(件)',
          key: 'quantity',
          align: 'center',
          width: 100,
          resizable: true
        },
        {
          title: '总重(千克)',
          key: 'weight',
          width: 120,
          resizable: true
        },
        {
          title: '运费(元)',
          key: 'cost',
          width: 90,
          resizable: true
        },
        {
          title: '备注',
          key: 'remark',
          minWidth: 200,
          resizable: true,
          render: (h, params) => {
            return h('div', {
              domProps: {
                innerHTML: params.row.remark.replace(/\n/g, '<br/>')
              }
            })
          }
        },
        {
          title: '操作',
          align: 'center',
          fixed: 'right',
          width: 160,
          render: (h, params) => {
            return h('div', [
              h(
                'Button',
                {
                  props: {
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px',
                    paddingTop: '5px',
                    paddingLeft: '10px',
                    paddingRight: '10px',
                    paddingBottom: '25px'
                  },
                  on: {
                    click: () => {
                      this.routeInfo = params.row.routes
                      this.showRouteInfo = true
                    }
                  }
                },
                '详情'
              ),
              h(
                'Button',
                {
                  props: {
                    type: 'success',
                    size: 'small'
                  },
                  style: {
                    paddingTop: '5px',
                    paddingLeft: '10px',
                    paddingRight: '10px',
                    paddingBottom: '25px'
                  },
                  on: {
                    click: () => {
                      this.currentOrderRoute = params.row
                      this.showRouteEditor = true
                    }
                  }
                },
                '编辑'
              )
            ])
          }
        }
      ]
    }
  },
  created () {
    this.getOrderRoutes(this.$route.params.order.id)
  },
  methods: {
    /**
     * 获取商品订单物流记录
     * @param {Object} orderId 商品订单ID
     */
    getOrderRoutes (orderId) {
      this.dataLoading = true
      listOrderRoutes(orderId)
        .then(res => {
          this.orderRoutes = res.data
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err)
          this.dataLoading = false
        })
    },
    /**
     * 打开商品订单物流记录编辑器
     */
    openOrderRouteEditor () {
      this.currentOrderRoute = defaultOrderRoute()
      this.currentOrderRoute.order = this.$route.params.order.id
      this.showRouteEditor = true
    },
    /**
     * 处理商品订单物流记录更新完成事件
     */
    handleOrderRouteUpdate () {
      this.getOrderRoutes(this.$route.params.order.id)
      this.showRouteEditor = false
      this.$emit('on-update')
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
