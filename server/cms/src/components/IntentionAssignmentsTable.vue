/* eslint-disable camelcase */
/* eslint-disable camelcase */
<template>
  <div v-if="this.$route.params.intention.flags == 0">
    <Button :loading="assignmentSubmitting" :disabled="assignmentNotSelected" type="primary" style="margin: 0 0 16px 0"
      @click="confirmSubmitAssignments">提交分配</Button>
    <Table :data="candidates" :columns="candidateFields" :loading="candidatesLoading || assignmentSubmitting" stripe
      border></Table>
  </div>
  <div v-else>
    <Button :loading="assignmentDropping" :disabled="this.$route.params.intention.flags != 1" type="primary" style="margin: 0 0 16px 0"
      @click="confirmDropAssignments">重新分配</Button>
    <Table :data="assignment" :columns="assignmentFields" :loading="assignmentsLoading" stripe border></Table>
  </div>
</template>

<script>
import {
  listRegisteredUsers
} from '@/api/user_api'
import {
  INTENTION_FLAGS,
  listIntentionAssignments,
  createIntetnionAssignments,
  dropIntentionAssignmentById,
  patchIntentionByFlags
} from '@/api/intention_api'
export default {
  name: 'IntentionAssignmentsTable',
  data () {
    return {
      /* 按钮状态 */
      assignmentNotSelected: true,
      assignmentSubmitting: false,
      assignmentDropping: false,

      /* 是否正在拉取列表数据 */
      candidatesLoading: false,
      assignmentsLoading: false,

      /* 用户模型列表 */
      candidates: [],

      assignment: [],

      assignmentExpired: false,

      /* 用户列表的字段定义 */
      candidateFields: [{
        // type: 'selection',
        align: 'center',
        width: 60,
        resizable: true,
        name: 'checkBox',
        render: (h, params) => {
          const self = this
          return h('div', [
            h('Checkbox', {
              props: {
                value: params.row.checkBox
              },
              on: {
                'on-change': (e) => {
                  self.candidates.forEach((items) => {
                    self.$set(items, 'checkBox', false)
                  })
                  console.log(e)
                  self.candidates[params.index].checkBox = e
                  console.log('选中的candidates信息')
                  console.log(self.candidates[params.index])

                  self.handleCandidatesSelection(self.candidates[params.index])
                }

              }
            })
          ])
        }
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
            'a', {
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
        title: '备注',
        align: 'center',
        minWidth: 200,
        resizable: true,
        render: (h, params) => {
          return h('Input', {
            props: {
              placeholder: '请输入备注...',
              value: params.row.remark
            },
            on: {
              'on-change': event => {
                params.row.remark = event.target.value
                this.candidates[params.index].remark = event.target.value
                const index = this.assignments.findIndex(a => {
                  return a.user.id === params.row.id
                })
                if (index >= 0) {
                  this.assignments[index].remark = event.target.value
                }
              }
            }
          })
        }
      }
      ],

      assignmentFields: [{
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
          const wx_name = params.row.user.wx_name
          const wx_mobile = params.row.user.mobile
          const wx_avatar_url = params.row.user.wx_avatar_url
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
        title: '真实姓名',
        align: 'center',
        width: 120,
        resizable: true,
        render: (h, params) => {
          return h('span', params.row.user.name)
        }
      },
      {
        title: '性别',
        align: 'center',
        width: 80,
        resizable: true,
        render: (h, params) => {
          return h('span', params.row.user.gender)
        }
      },
      {
        title: '联系电话',
        align: 'center',
        width: 160,
        resizable: true,
        render: (h, params) => {
          return h('span', params.row.user.phone)
        }
      },
      {
        title: '电子邮件',
        align: 'center',
        minWidth: 200,
        resizable: true,
        render: (h, params) => {
          const email = params.row.user.email
          return h(
            'a', {
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
        title: '分配时间',
        key: 'created_at',
        align: 'center',
        width: 120,
        resizable: true
      },
      {
        title: '超时天数',
        align: 'center',
        width: 110,
        resizable: true,
        render: (h, params) => {
          return h(
            'span', {
              style: {
                color: 'red'
              }
            },
            params.row.expired_days
          )
        }
      },
      {
        title: '备注',
        key: 'remark',
        minWidth: 200,
        resizable: true
      }
      ]
    }
  },
  created () {
    if (this.$route.params.intention.flags === INTENTION_FLAGS.UNASSIGNED) {
      this.getCandidates()
    } else {
      this.getIntentionAssignments(this.$route.params.intention.id)
    }
  },
  methods: {
    handleCandidatesSelection (selectedCandidate) {
      const intentionId = this.$route.params.intention.id

      var postData = {
        remark: selectedCandidate.remark,
        intention: intentionId,
        user: selectedCandidate.id

      }
      console.log('这里是POST请求的数据')
      console.log(postData)
      this.assignment.push(postData)

      this.assignmentNotSelected = false
    },
    getCandidates () {
      this.candidatesLoading = true
      listRegisteredUsers()
        .then(res => {
          this.candidates = res.data.results
          this.candidates.forEach(item => {
            item._checked = false
            item.remark = ''
          })
          this.candidatesLoading = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.candidatesLoading = false
        })
    },
    getIntentionAssignments (intentionId) {
      listIntentionAssignments(intentionId)
        .then(res => {
          this.candidates = []
          this.assignment = res.data
          this.assignmentExpired = this.assignment.some(item => {
            return item.expired_days > 0
          })

          this.assignmentsLoading = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.assignmentsLoading = false
        })
    },
    confirmSubmitAssignments () {
      this.assignmentSubmitting = true
      this.$Modal.confirm({
        title: '操作确认',
        content: '确定提交分配信息？',
        onOk: () => {
          this.submitAssignments()
        },
        onCancel: () => {
          this.assignmentSubmitting = false
        }
      })
    },
    submitAssignments () {
      const intentionId = this.$route.params.intention.id
      createIntetnionAssignments(intentionId, this.assignment[0])
        .then(() => {
          console.log('输出信息')
          console.log(this.assignment)
          this.assignmentNotSelected = true
          this.getIntentionAssignments(this.$route.params.intention.id)
          this.$route.params.intention.flags = INTENTION_FLAGS.ASSIGNED
          this.assignmentSubmitting = false
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.assignmentSubmitting = false
        })
    },
    confirmDropAssignments () {
      this.assignmentDropping = true
      this.$Modal.confirm({
        title: '操作确认',
        content: '确定重新分配？',
        onOk: () => {
          this.dropAssignment()
        },
        onCancel: () => {
          this.assignmentDropping = false
        }
      })
    },
    dropAssignment () {
      // const intentionId = this.$route.params.intention.id
      var assignmentPopped = this.assignment.pop()
      dropIntentionAssignmentById(assignmentPopped.id)
        .then(() => {
          this.getCandidates()
          this.$route.params.intention.flags = INTENTION_FLAGS.UNASSIGNED

          patchIntentionByFlags(this.$route.params.intention.id, INTENTION_FLAGS.UNASSIGNED)
            .then(res => {
              this.assignmentDropping = false
            })
            .catch(err => {
              this.$Message.error(err.toString())
              this.assignmentDropping = false
            })
        })
        .catch(err => {
          this.$Message.error(err.toString())
          this.assignmentDropping = false
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

<style></style>
