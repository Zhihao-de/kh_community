import axios from 'axios'

export const USER_FLAGS = {
  WAITING_FOR_APPROVAL: 0,
  SIGNING: 1,
  REGISTERED: 2,
  BANNED: 3
}

export const USER_APPLICATION_FLAGS = {
  WAITING_FOR_APPROVAL: 0,
  ACCEPT: 1,
  REJECT: 2
}

/**
 * 获取用户状态名
 * @param flags 用户状态
 * @returns {*}
 */
export function getUserFlagsText (flags) {
  return flags === USER_FLAGS.WAITING_FOR_APPROVAL
    ? '已申请'
    : flags === USER_FLAGS.SIGNING
      ? '待签协议'
      : flags === USER_FLAGS.REGISTERED
        ? '已注册'
        : '暂停'
}

/**
 * 获取用户状态颜色
 * @param flags 用户状态
 * @returns {*}
 */
export function getUserFlagsColor (flags) {
  return flags === USER_FLAGS.WAITING_FOR_APPROVAL
    ? '#19be6b' /* 已申请 */
    : flags === USER_FLAGS.SIGNING
      ? '#ff9900' /* 待签协议 */
      : flags === USER_FLAGS.REGISTERED
        ? '#2d8cf0' /* 已注册 */
        : '#FF4040'
  /* 暂停 */
}

/**
 * 获取留言订单的状
 * @param flags 留言订单状态
 * @returns {*}
 */
export function getUserAppFlagsText (flags) {
  return flags === USER_APPLICATION_FLAGS.WAITING_FOR_APPROVAL
    ? '待审批'
    : flags === USER_APPLICATION_FLAGS.ACCEPT
      ? '同意'
      : '不同意'
}

/**
 * 获取产品状态的颜色
 * @param flags 产品状态
 * @returns {*}
 */
export function getUserAppFlagsColor (flags) {
  return flags === USER_APPLICATION_FLAGS.WAITING_FOR_APPROVAL
    ? '#2d8cf0' /* 待审批 */
    : flags === USER_APPLICATION_FLAGS.ACCEPT
      ? '#19be6b' /* 同意 */
      : '#FF4040'
  /* 不同意 */
}

/**
 * 获取分页用户模型列表
 * @param page 页索引
 * @returns {*}
 */
export function listUsers (page) {
  return axios
    .get('/users/', {
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

export function listRegisteredUsers () {
  return axios
    .get('/users/?page_size=10000&flags=' + USER_FLAGS.REGISTERED)
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
 * 获取分页用户模型列表
 * @param userId 用户id
 * @returns {*}
 */
export function listUserApplications (userId) {
  return axios.get('/users/' + userId + '/applications').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 获取分页用户文档模型列表
 * @param userId 用户id
 * @returns {*}
 */
export function listUserDocs (userId) {
  return axios.get('/users/' + userId + '/docs').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 更新用户状态
 * @param userId 用户id
 * @param flags 用户状态
 * @returns {*}
 */
export function patchUserByFlags (userId, flags) {
  return axios
    .patch('/users/' + userId + '/', {
      id: userId,
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
 * 获取用户位置
 * @param userId 用户id
 * @returns {*}
 */





/**
 * 获取用户位置
 * @param userId 用户id
 * @returns {*}
 */
export function getUserLocation (userId) {
  return axios.get('/users/' + userId + '/locations/').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 更新用户位置
 * @param loc 用户位置对象
 * @returns {*}
 */
export function postUserLocation (loc) {
  return axios.post('/users/' + loc.user + '/locations/', loc).then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

export const TMAP_KEY = 'MQCBZ-PPLCD-E6R4G-PPXQS-FJCHV-B7BOP'

export function getTMap () {
  return new Promise(function (resolve, reject) {
    window.initMap = function () {
      resolve(window.TMap)
    }
    var script = document.createElement('script')
    script.type = 'text/javascript'
    script.async = true
    script.src =
      'https://map.qq.com/api/gljs?v=1.exp&callback=initMap&key=' + TMAP_KEY
    script.onerror = reject
    document.head.appendChild(script)
  })
}
