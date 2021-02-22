<template>
  <div>
    <Table :data="userApplications" :columns="userApplicationFields" :loading="dataLoading" stripe border></Table>
    <Modal title="查看图片" v-model="showImageViewer" :footer-hide="true">
      <img :src="imageURL" v-if="showImageViewer" style="width: 100%" />
    </Modal>
  </div>
</template>

<script>
import {
  USER_APPLICATION_FLAGS,
  getUserAppFlagsText,
  getUserAppFlagsColor,
  listUserApplications,
  patchUserByFlags
} from '@/api/user_api'

/**
   * 产品用户列表
   */
export default {
  name: 'UserApplicationsTable',

  data () {
    const _this = this
    return {
      /* 是否正在拉取列表数据 */
      dataLoading: false,

      /* 用户申请模型列表 */
      userApplications: [],

      showImageViewer: false,

      imageURL: '',

      /* 用户列表的字段定义 */
      userApplicationFields: [{
        type: 'index',
        align: 'center',
        width: 60,
        resizable: true
      },
      {
        title: '真实姓名',
        key: 'name',
        align: 'center',
        width: 140,
        resizable: true
      },
      {
        title: '性别',
        align: 'center',
        key: 'gender',
        width: 80,
        resizable: true
      },
      {
        title: '联系电话',
        align: 'center',
        key: 'phone',
        width: 160,
        resizable: true
      },
      {
        title: '电子邮件',
        key: 'email',
        minWidth: 200,
        resizable: true
      },
      {
        title: '身份证明',
        align: 'center',
        width: 180,
        resizable: true,
        render: (h, params) => {
          return h('div', [
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
                    this.imageURL = params.row.idc_front_pic_url
                    this.showImageViewer = true
                  }
                }
              },
              '正面'
            ),
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
                    this.imageURL = params.row.user.idc_back_pic_url
                    this.showImageViewer = true
                  }
                }
              },
              '反面'
            )
          ])
        }
      },
      {
        title: '拒绝原因',
        key: 'reason_of_refusal',
        minWidth: 200,
        resizable: true
      },
      {
        title: '状态',
        key: 'flags',
        align: 'center',
        width: 150,
        sortable: true,
        resizable: true,
        render: (h, params) => {
          return h(
            'Tag', {
              props: {
                type: 'dot',
                color: getUserAppFlagsColor(params.row.flags)
              }
            },
            getUserAppFlagsText(params.row.flags)
          )
        }
      },
      {
        title: '操作',
        key: 'operations',
        resizable: true,
        align: 'center',
        width: 150,
        sortable: true,

        render: (h, params) => {
          return h('div', [
            h('Button', {
              props: {
                type: 'primary',
                shape: 'circle',
                icon: 'md-checkmark',
                size: 'small'
              },
              style: {
                marginRight: '5px'
              },
              on: {
                click: () => {
                  _this.updateUserApplicationByFlags(params.row, USER_APPLICATION_FLAGS.ACCEPT)
                }
              }
            }),
            h('Button', {
              props: {
                type: 'error',
                icon: 'md-close',
                shape: 'circle',
                size: 'small'
              },
              on: {
                click: () => {
                  // 状态更新为不同意

                  _this.updateUserApplicationByFlags(params.row, USER_APPLICATION_FLAGS.REJECT)
                }
              }
            })

          ])
          //   }
        }
      }
      ]
    }
  },
  created () {
    this.getUserApplications(this.$route.params.user.id)
  },
  methods: {
    getUserApplications (userId) {
      this.dataLoading = true
      listUserApplications(userId)
        .then(res => {
          this.userApplications = res.data
          this.dataLoading = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.dataLoading = false
        })
    },
    /**
       * 更新留言订单状态
       * @param intention 当前产品模型
       * @param flags 订单状态
       * @returns {*}
       */
    updateUserApplicationByFlags (currentUserApplication, flags) {
      const oldFlagsColor = getUserAppFlagsColor(currentUserApplication.flags)
      const newFlagsColor = getUserAppFlagsColor(flags)
      this.$Modal.confirm({
        title: '操作确认',
        content: '确定将用户 <strong>' +
            this.$route.params.user.wx_name +
            "</strong> 的申请状态从 <font color='" +
            oldFlagsColor +
            "'>" +
            getUserAppFlagsText(currentUserApplication.flags) +
            "</font> 转变为 <font color='" +
            newFlagsColor +
            "'>" +
            getUserAppFlagsText(flags) +
            '</font> ？',
        onOk: () => {
          this.dataLoading = true
          patchUserByFlags(currentUserApplication.user, flags)
            .then(() => {
              currentUserApplication.flags = flags
              this.$Message.info('操作成功！')
              this.dataLoading = false
            })
            .catch(err => {
              this.$Message.error(err.toString())
              this.dataLoading = false
            })
        }
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
