<template>
  <Table
    :data="intentionDetails"
    :columns="intentionDetailFields"
    :loading="dataLoading"
    stripe
    border
  ></Table>
</template>

<script>
import { listIntentionDetails } from '@/api/intention_api'

export default {
  name: 'IntentionDetailsTable',
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 留言订单详情列表 */
      intentionDetails: [],

      /* 产品列表的字段定义 */
      intentionDetailFields: [
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
          title: '指导价(元)',
          align: 'center',
          width: 130,
          resizable: true,
          render: (h, params) => {
            return h('span', params.row.product.retail_price)
          }
        }
      ]
    }
  },
  created () {
    this.getIntentionDetails(this.$route.params.intention.id)
  },
  methods: {
    getIntentionDetails (intentionId) {
      this.dataLoading = true
      listIntentionDetails(intentionId)
        .then(res => {
          this.intentionDetails = res.data
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
