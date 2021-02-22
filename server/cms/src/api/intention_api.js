import axios from 'axios'

export const INTENTION_FLAGS = {
  UNASSIGNED: 0,
  ASSIGNED: 1,
  CANCELLED: 2,
  COMPLETED: 3,
  MISSED: 4
}

export const INTENTION_ASSIGNMENT_FLAGS = {
  NORMAL: 0,
  EXPIRED: 1,
  DROPPED: 2
}

/**
 * 获取留言订单的状态名
 * @param flags 留言订单状态
 * @returns {*}
 */
export function getFlagsText(flags) {
  return flags === INTENTION_FLAGS.UNASSIGNED ?
    '待分配' :
    flags === INTENTION_FLAGS.ASSIGNED ?
    '已分配' :
    flags === INTENTION_FLAGS.COMPLETED ?
    '已完成' :
    flags === INTENTION_FLAGS.CANCELLED ?
    '已取消' :
    '无法联系'
}

/**
 * 获取留言订单状态的颜色
 * @param flags 留言订单状态
 * @returns {*}
 */
export function getFlagsColor(flags) {
  return flags === INTENTION_FLAGS.UNASSIGNED ?
    '#ff9900' /* 待分配 */ :
    flags === INTENTION_FLAGS.ASSIGNED ?
    '#2d8cf0' /* 已分配 */ :
    flags === INTENTION_FLAGS.COMPLETED ?
    '#19be6b' /* 已完成 */ :
    flags === INTENTION_FLAGS.CANCELLED ?
    '#e6e6fa' /* 已取消 */ :
    '#FF4040'
  /* 超时订单 */
}

/**
 * 获取留言订单的列表
 * @param page 页索引
 * @returns {*}
 */
export function listIntentions(page) {
  return axios
    .get('/intentions', {
      params: {
        page: page
      }
    })
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
}

/**
 * 获取留言订单
 * @param orderId 留言订单ID
 * @returns {*}
 */
export function getIntention(intentionId) {
  return axios.get('/intentions/' + intentionId + '/').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 获取留言订单
 * @param orderId 留言订单ID
 * @param orderId 新的flags
 * @returns {*}
 */
export function patchIntentionByFlags(intentionId, flags) {
  return axios
    .patch('/intentions/' + intentionId + '/', {
      id: intentionId,
      flags: flags
    })
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
}

/**
 * 获取留言订单的详情product的信息（可能是多个）
 * @returns {*}
 */
export function listIntentionDetails(intentionId) {
  return axios.get('/intentions/' + intentionId + '/details/').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 获取留言订单的历史信息（可能是多个）
 * @returns {*}
 */
export function listIntentionHistory(intentionId) {
  return axios.get('/intentions/' + intentionId + '/history/').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}



/**
 * 获取留言订单的分配记录
 * @param intentionId 留言订单ID
 * @returns {*}
 */
export function listIntentionAssignments(intentionId) {
  return axios.get('/intentions/' + intentionId + '/assignments/').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 创建留言订单的分配
 * @param intentionId 留言订单ID
 * @param assignments 留言订单分配对象
 * @returns {*}
 */
export function createIntetnionAssignments(intentionId, assignment) {
  return axios
    .post('/intentions/' + intentionId + '/assignments/', assignment)
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
}

/**
 * 更改留言订单的分配状态为 DROPPED
 * @param intentionId 留言订单ID
 * @param assignments 留言订单分配对象
 * @returns {*}
 */
export function dropIntetnionAssignments(intentionId, assignments) {
  const data = assignments.map(a => {
    var flags = a.flags
    // 如果分配状态为超时则保留，否则设置为 DROPPED
    if (flags !== INTENTION_ASSIGNMENT_FLAGS.EXPIRED) {
      flags = INTENTION_ASSIGNMENT_FLAGS.DROPPED
    }
    return {
      id: a.id,
      flags: flags
    }
  })
  return axios
    .patch('/intentions/' + intentionId + '/assignments/drop', data)
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
}
 /* 更改留言订单的分配状态为 DROPPED
 * @param intentionId 留言订单ID
 * @param assignments 留言订单分配对象
 * @returns {*}
 */
export function dropIntentionAssignmentById(id) {
  return axios
    .delete('/intentions/assignments/' + id+'/')
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
}

 /* 增加留言订单历史
 * @param intentionId 留言订单ID
 * @param history 留言订单历史对象
 * @returns {*}
 */
export function createIntentionHistory(intentionId, history){
  return axios
    .post('/intentions/' + intentionId + '/history/', history)
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )

}
