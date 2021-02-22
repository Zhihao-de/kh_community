<template>
  <Table :data="IntentionHistory" :columns="intentionHistoryFields" :loading="dataLoading" stripe border></Table>
</template>

<script>
import {
  getFlagsText,
  getFlagsColor,
  listIntentionHistory
} from '@/api/intention_api'

export default {
  name: 'IntentionHistoryTable',
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 留言订单详情列表 */
      IntentionHistory: [],

      /* 产品列表的字段定义 */
      intentionHistoryFields: [{
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
                color: getFlagsColor(params.row.flags)
              }
            },
            getFlagsText(params.row.flags)
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
        title: '客户微信',
        minWidth: 240,
        resizable: true,
        render: (h, params) => {
          const wx_name = params.row.wx_name
          const wx_mobile = params.row.wx_mobile
          const wx_avatar_url = params.row.wx_avatar_url
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
        title: '客户姓名',
        key: 'name',
        align: 'center',
        width: 120,
        resizable: true
      },
      {
        title: '联系电话',
        key: 'phone',
        align: 'center',
        width: 150,
        resizable: true
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
  created () {
    this.getIntentionHistory(this.$route.params.intention.id)
  },
  methods: {
    getIntentionHistory (intentionId) {
      this.dataLoading = true
      listIntentionHistory(intentionId)
        .then(res => {
          this.IntentionHistory = res.data
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
