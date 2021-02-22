import axios from 'axios'

export const ORDER_FLAGS = {
  UNPAID: 0,
  PAID: 1,
  DELIVERED: 2,
  RECEIVED: 3,
  CANCELLED: 4,
  REFUNDING: 5,
  REFUNDED:6,
}

export const PAYMENT_METHODS = {
  ALIPAY: 0,
  WWCHAT_PAY: 1,
  UNION_PAY: 2,
  OTHER: 3
}

export function defaultOrderRoute () {
  return {
    id: -1,
    list_amount:0,
    tare:0.00,
    PAYMENT_METHODS:1,
    is_paid:true,
    transaction_id:'None',
    paid_at:'0',
    refund:0,
    flags:0,
    created_at:'',
    updated_at:'',
    user:-1,
    order:-1
  }
}
export function defaultOrderHistory () {
  return {
    id: -1,
    express: '',
    receipt_no: '',
    address: '',
    quantity: 1,
    weight: 0,
    cost: 0,
    remark: '',
    order: -1
  }
}


/**
 * 获取商品订单的状态
 * @param flags 商品订单状态
 * @returns {*}
 */
export function getOrderFlagsText (flags) {
  return flags === ORDER_FLAGS.UNPAID
    ? '未付款'
    : flags === ORDER_FLAGS.PAID
      ? '已付款'
      : flags === ORDER_FLAGS.DELIVERED
        ? '配送中'
        : flags === ORDER_FLAGS.RECEIVED
          ? '已签收'
          : flags === ORDER_FLAGS.CANCELLED
            ? '已取消'
            : flags === ORDER_FLAGS.REFUNDING
              ? '退款中'

            : '已退款'
}

/**
 * 获取支付方法的名称
 * @param method 支付方法
 * @returns {*}
 */
export function getPaymentMethodText (method) {
  return method === PAYMENT_METHODS.ALIPAY
    ? '支付宝'
    : method === PAYMENT_METHODS.WWCHAT_PAY
      ? '微信支付'
      : method === PAYMENT_METHODS.UNION_PAY
        ? '银行卡'
        : '其他'
}

/**
 * 获取订单状态的颜色
 * @param flags 订单状态
 * @returns {*}
 */
export function getOrderFlagsColor (flags) {
  return flags === ORDER_FLAGS.UNPAID
    ? '#ff4040' /* 未付款 */
    : flags === ORDER_FLAGS.PAID
      ? '#ff9900' /* 已付款 */
      : flags === ORDER_FLAGS.DELIVERED
        ? '#2d8cf0' /* 配送中 */
        : flags === ORDER_FLAGS.RECEIVED
          ? '#19be6b' /* 已签收 */
          : flags === ORDER_FLAGS.CANCELLED
            ? '#ff4040' /* 已取消 */
            : '#e6e6fa'
  /* 已退款 */
}

/**
 * 获取分页的商品订单列表
 * @param page 页索引
 * @returns {*}
 */
export function listOrders (page) {
  return axios
    .get('/orders', {
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
 * 获取商品订单
 * @param orderId 商品订单ID
 * @returns {*}
 */
export function getOrder (orderId) {
  return axios.get('/orders/' + orderId + '/').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 更新商品订单状态
 * @param orderId 商品订单ID
 * @param flags 商品订单状态
 * @returns {*}
 */
export function patchOrderByFlags (orderId, flags) {
  return axios
    .patch('/orders/' + orderId + '/', {
      orderId: orderId,
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
 * 获取某订单的交易记录(1:n)
 * @param orderId 订单id
 * @returns {*}
 */
export function listOrderTranscations (orderId) {
  return axios.get('/orders/' + orderId + '/transactions').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

export function patchOrderTransactionByRefund (orderTransactionModel) {
  return axios
    .patch(
      '/orders/' +
      orderTransactionModel.order +
      '/transactions/' +
      orderTransactionModel.id +
      '/',
      orderTransactionModel
    )
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
}


export function refund() {
  return axios
    .post(
      '/orders/' +
      orderTransactionModel.order +
      '/transactions/' +
      orderTransactionModel.id +
      '/',
      orderTransactionModel
    )
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
 * 获取订单的商品清单(1:n)
 * @param orderId 订单id
 * @returns {*}
 */
export function listOrderDetails (orderId) {
  return axios.get('/orders/' + orderId + '/details').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 获取订单的物流记录(1:n)
 * @param orderId 订单id
 * @returns {*}
 */
export function listOrderRoutes (orderId) {
  return axios.get('/orders/' + orderId + '/routes').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}
/**
 * 获取订单的订单记录(1:n)
 * @param orderId 订单id
 * @returns {*}
 */
export function listOrderHistory (orderId) {
  return axios.get('/orders/' + orderId + '/history').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}



/**
 * 创建或更新订单物流
 * @param {Object} orderRouteModel
 */
export function postOrPatchOrderRoute (orderRouteModel) {
  var request = '/orders/' + orderRouteModel.order + '/routes/'
  if (orderRouteModel.id > 0) {
    return axios
      .patch(request + orderRouteModel.id + '/', orderRouteModel)
      .then(
        res => {
          return Promise.resolve(res)
        },
        err => {
          return Promise.reject(err)
        }
      )
  } else {
    return axios.post(request, orderRouteModel).then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
  }
}

export function listOrdersHistory (orderId) {
  return axios
    .get('/order_history', {
      params: {
        order_id: orderId
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


 /* 增加订单历史
 * @param orderId 订单ID
 * @param history 留言订单历史对象
 * @returns {*}
 */
export function createOrderHistory(orderId, history){
  return axios
    .post('/orders/' + orderId + '/history/', history)
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )

}
