import request from './index'

export const paymentApi = {
  // 创建支付订单
  createOrder(data) {
    return request.post('/payment/create-order', data)
  },

  // 支付宝支付
  alipayPayment(data) {
    return request.post('/payment/alipay', data)
  },

  // 微信支付
  wechatPayment(data) {
    return request.post('/payment/wechat', data)
  },

  // PayPal支付
  paypalPayment(data) {
    return request.post('/payment/paypal', data)
  },

  // 联系管理员支付
  adminPayment(data) {
    return request.post('/payment/admin', data)
  },

  // 查询支付状态
  queryPaymentStatus(orderId) {
    return request.get(`/payment/status/${orderId}`)
  },

  // 获取支付方式列表
  getPaymentMethods() {
    return request.get('/payment/methods')
  }
}
