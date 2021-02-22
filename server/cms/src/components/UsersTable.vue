<template>
  <div>
    <Table
      :data="users"
      :columns="userFields"
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
import {
  USER_FLAGS,
  getUserFlagsText,
  getUserFlagsColor,
  listUsers,
  patchUserByFlags
} from '@/api/user_api'

/**
 * 产品用户列表
 */
export default {
  name: 'UsersTable',
  data () {
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 用户总数，用于设置分页器 */
      count: 0,

      /* 用户模型列表 */
      users: [],

      /* 用户列表的字段定义 */
      userFields: [
        {
          type: 'index',
          align: 'center',
          width: 60,
          resizable: true
        },
        {
          title: '用户微信',
          minWidth: 240,
          resizable: true,
          render: (h, params) => {
            const wx_name = params.row.wx_name
            const wx_mobile = params.row.mobile
            const wx_avatar_url = params.row.wx_avatar_url
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
          title: '真实姓名',
          key: 'name',
          align: 'center',
          width: 120,
          resizable: true
        },
        {
          title: '性别',
          key: 'gender',
          align: 'center',
          width: 80,
          resizable: true
        },
        {
          title: '联系电话',
          key: 'phone',
          align: 'center',
          width: 160,
          resizable: true
        },
        {
          title: '电子邮件',
          align: 'center',
          minWidth: 200,
          resizable: true,
          render: (h, params) => {
            const email = params.row.email
            return h(
              'a',
              {
                attrs: {
                  href: 'mailto:' + email
                }
              },
              email
            )
          }
        },
        {
          title: '位置',
          align: 'center',
          width: 160,
          resizable: true,
          render: h => {
            return h('span', '建设中...')
          }
        },
        {
          title: '注册时间',
          key: 'created_at',
          align: 'center',
          width: 180,
          resizable: true
        },
        {
          title: '最后登录时间',
          key: 'logined_at',
          align: 'center',
          width: 180,
          resizable: true
        },
        {
          title: '状态',
          align: 'center',
          width: 140,
          sortable: true,
          resizable: true,
          render: (h, params) => {
            return h(
              'Tag',
              {
                props: {
                  type: 'dot',
                  color: getUserFlagsColor(params.row.flags)
                }
              },
              getUserFlagsText(params.row.flags)
            )
          },
          filters: [
            {
              label: '已申请',
              value: USER_FLAGS.WAITING_FOR_APPROVAL
            },
            {
              label: '待签协议',
              value: USER_FLAGS.SIGNING
            },
            {
              label: '已注册',
              value: USER_FLAGS.REGISTERED
            },
            {
              label: '暂停',
              value: USER_FLAGS.BANNED
            }
          ],
          filterMethod (value, row) {
            return row.flags === value
          }
        },
        {
          title: '操作',
          fixed: 'right',
          align: 'center',
          width: 140,
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
                        name: 'user_view',
                        params: { user: params.row }
                      })
                    }
                  }
                },
                '详情'
              )
            ]
            if (params.row.flags === USER_FLAGS.WAITING_FOR_APPROVAL) {
              children.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.$router.push({
                          name: 'user_view',
                          params: { user: params.row }
                        })
                      }
                    }
                  },
                  '审批'
                )
              )
            } else if (params.row.flags === USER_FLAGS.REGISTERED) {
              children.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'warning',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        // 状态更新为暂停
                        this.updateUserByFlags(params.row, USER_FLAGS.BANNED)
                      }
                    }
                  },
                  '暂停'
                )
              )
            } else if (params.row.flags === USER_FLAGS.BANNED) {
              children.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'warning',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.updateUserByFlags(
                          params.row,
                          USER_FLAGS.REGISTERED
                        )
                      }
                    }
                  },
                  '恢复'
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
    this.getUsers(1)
  },
  methods: {
    getUsers (page) {
      this.dataLoading = true
      listUsers(page)
        .then(res => {
          this.users = res.data.results
          this.count = res.data.count
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.dataLoading = false
        })
    },
    /**
     * 更新用户状态
     * @param currentUser 当前用户对象
     * @param flags 用户状态
     * @returns {*}
     */
    updateUserByFlags (currentUser, flags) {
      console.log(currentUser.flags)
      const oldFlagsColor = getUserFlagsColor(currentUser.flags)
      const newFlagsColor = getUserFlagsColor(flags)
      this.$Modal.confirm({
        title: '操作确认',
        content:
          '确定将用户 <strong>' +
          currentUser.wx_name +
          "</strong> 的状态从 <font color='" +
          oldFlagsColor +
          "'>" +
          getUserFlagsText(currentUser.flags) +
          "</font> 转变为 <font color='" +
          newFlagsColor +
          "'>" +
          getUserFlagsText(flags) +
          '</font> ？',
        onOk: () => {
          this.dataLoading = true
          patchUserByFlags(currentUser.id, flags)
            .then(() => {
              currentUser.flags = flags
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
      this.getUsers(page)
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
