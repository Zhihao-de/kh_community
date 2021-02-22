<template>
  <div>
    <Table
      :data="docs"
      :columns="docFields"
      :loading="dataLoading"
      stripe
      border
    ></Table>
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
import { listUserDocs } from '@/api/user_api'

/**
 * 产品用户列表
 */
export default {
  name: 'UserDocsTable',
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 用户总数，用于设置分页器 */
      count: 0,

      /* 用户文档模型列表 */
      docs: [],

      /* 用户文档列表的字段定义 */
      docFields: [
        {
          type: 'index',
          align: 'center',
          width: 60,
          resizable: true
        },
        {
          title: '文档名称',
          key: 'file_name',
          align: 'center',
          width: 200,
          resizable: true
        },
        {
          title: '文档链接',
          align: 'center',
          minWidth: 200,
          resizable: true,
          render: (h, params) => {
            return h(
              'a',
              {
                attrs: {
                  href: params.row.file_url,
                  target: '_blank'
                }
              },
              params.row.file_url
            )
          }
        },
        {
          title: '创建时间',
          key: 'created_at',
          align: 'center',
          width: 180,
          resizable: true
        },
        {
          title: '修改时间',
          key: 'updated_at',
          align: 'center',
          width: 180,
          resizable: true
        },
        {
          title: '操作',
          fixed: 'right',
          align: 'center',
          width: 140
        }
      ]
    }
  },
  created () {
    this.getUserDocs(1)
  },
  methods: {
    getUserDocs (page) {
      const userId = this.$route.params.user.id
      this.dataLoading = true
      listUserDocs(userId, page)
        .then(res => {
          this.docs = res.data.results
          this.count = res.data.count
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.dataLoading = false
        })
    },
    /**
     * 换页的事件处理
     * @param page 页索引
     * @returns {*}
     */
    onPageChanged (page) {
      this.getUserDocs(page)
    }
  }
}
</script>

<style scoped></style>
