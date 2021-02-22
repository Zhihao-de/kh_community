<template>
  <div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>订单信息</strong></p>
        <Button slot="extra" icon="md-refresh" @click="refreshIntention"></Button>
        <Table :data="intentionDetails" :columns="intentionDetailsFields" stripe border>
        </Table>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>用户分配</strong></p>
        <IntentionAssignmentsTable></IntentionAssignmentsTable>
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>商品清单</strong></p>
        <IntentionDetailsTable></IntentionDetailsTable>
      </Card>
    </div>
    <div style="padding: 20px" v-if="this.$route.params.intention.message !== null">
      <Card :bordered="false">
        <p slot="title"><strong>客户留言</strong></p>
        {{ this.$route.params.intention.message }}
      </Card>
    </div>
    <div style="padding: 20px">
      <Card :bordered="false">
        <p slot="title"><strong>历史记录</strong></p>
        <IntentionHistoryTable></IntentionHistoryTable>
      </Card>
    </div>
  </div>
</template>

<script>
import {
  getFlagsText,
  getFlagsColor,
  getIntention
} from '@/api/intention_api'
import IntentionDetailsTable from '@/components/IntentionDetailsTable'
import IntentionAssignmentsTable from '@/components/IntentionAssignmentsTable'
import IntentionHistoryTable from '@/components/IntentionHistoryTable'

export default {
  name: 'IntentionDetailView',
  components: {
    IntentionDetailsTable,
    IntentionAssignmentsTable,
    IntentionHistoryTable
  },
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      intentionId: this.$route.params.intention.id,

      /* 商品订单详情列表 */
      intentionDetails: [this.$route.params.intention],

      /* 商品订单列表的字段定义 */
      intentionDetailsFields: [{
        title: '状态',
        key: 'flags',
        align: 'center',
        width: 130,
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
        title: '数量(件)',
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
    getIntentionById (intentionId) {
      this.dataLoading = true
      getIntention(intentionId)
        .then(res => {
          this.$route.params.intention = res.data
          this.intentions = [res.data]
          this.dataLoading = false
        })
        .catch(err => {
          this.dataLoading = false
          this.$Message.error(err.toString())
        })
    },
    refreshIntention () {
      if (this.dataLoading) {
        this.$Message.error('请勿频繁刷新！')
        return
      }
      this.getIntentionById(this.intentionId)
    }
  }
}
</script>

<style scoped></style>
