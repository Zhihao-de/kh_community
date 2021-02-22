<template>
  <div>
    <Table :data="intentions" :columns="intentionFields" :loading="dataLoading" stripe border>
    </Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <Page :page-size="4" :total="count" :current="1" @on-change="onPageChanged"></Page>
      </div>
    </div>
  </div>
</template>

<script>
/* 导入Intentions的信息
   */
import {
  INTENTION_FLAGS,
  getFlagsText,
  getFlagsColor,
  listIntentions,
  patchIntentionByFlags
} from '@/api/intention_api'

/**
   * 留言订单列表
   */
export default {
  name: 'IntentionsTable',

  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 产品总数，用于设置分页器 */
      count: 0,

      /* Intention留言订单列表 */
      intentions: [],

      /* 产品列表的字段定义 */
      intentionFields: [{
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
      },
      {
        title: '操作',
        fixed: 'right',
        align: 'center',
        minWidth: 300,
        resizable: true,
        render: (h, params) => {
          var children = [
            h(
              'Button', {
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
                      name: 'intention_view',
                      params: {
                        intention: params.row
                      }
                    })
                  }
                }
              },
              '详情'
            )
          ]
          if (params.row.flags === 0 /* 待分配 */) {
            children.push(
              h(
                'Button', {
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
                        name: 'intention_view',
                        params: {
                          intention: params.row
                        }
                      })
                      console.log(params.row)
                    }
                  }
                },
                '分配'
              )
            )
            children.push(
              h(
                'Button', {
                  props: {
                    type: 'warning',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.updateIntentionByFlags(
                        params.row,
                        INTENTION_FLAGS.COMPLETED
                      )
                    }
                  }
                },
                '完成'
              )
            )
            children.push(
              h(
                'Button', {
                  props: {
                    type: 'warning',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.updateIntentionByFlags(
                        params.row,
                        INTENTION_FLAGS.CANCELLED
                      )
                    }
                  }
                },
                '取消'
              )
            )
            children.push(
              h(
                'Button', {
                  props: {
                    type: 'warning',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.updateIntentionByFlags(
                        params.row,
                        INTENTION_FLAGS.MISSED
                      )
                    }
                  }
                },
                '失联'
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
    this.getIntentions(1)
  },
  methods: {
    getIntentions (page) {
      this.dataLoading = true
      listIntentions(page)
        .then(res => {
          this.intentions = res.data.results
          this.count = res.data.count
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err)
          this.dataLoading = false
        })
    },
    /**
       * 更新留言订单状态
       * @param currentIntention 当前留言订单模型
       * @param flags 新的留言订单状态
       * @returns {*}
       */
    updateIntentionByFlags (currentIntention, flags) {
      if (currentIntention.flags === flags) return
      const oldFlagsColor = getFlagsColor(currentIntention.flags)
      const newFlagsColor = getFlagsColor(flags)
      this.$Modal.confirm({
        title: '操作确认',
        content: '确定将留言订单 <strong>' +
            currentIntention.id +
            "</strong> 的状态从 <font color='" +
            oldFlagsColor +
            "'>" +
            getFlagsText(currentIntention.flags) +
            "</font> 转变为 <font color='" +
            newFlagsColor +
            "'>" +
            getFlagsText(flags) +
            '</font> ？',
        onOk: () => {
          this.dataLoading = true
          patchIntentionByFlags(currentIntention.id, flags)
            .then(() => {
              currentIntention.flags = flags
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
      this.getIntentions(page)
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
