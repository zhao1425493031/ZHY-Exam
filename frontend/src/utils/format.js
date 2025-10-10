// 格式化工具函数
import dayjs from 'dayjs'

/**
 * 格式化日期
 * @param {string|Date} date 日期
 * @param {string} format 格式，默认为 'YYYY-MM-DD HH:mm:ss'
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (date, format = 'YYYY-MM-DD HH:mm:ss') => {
  if (!date) return ''
  return dayjs(date).format(format)
}

/**
 * 格式化相对时间
 * @param {string|Date} date 日期
 * @returns {string} 相对时间字符串
 */
export const formatRelativeTime = (date) => {
  if (!date) return ''
  return dayjs(date).fromNow()
}

/**
 * 格式化文件大小
 * @param {number} bytes 字节数
 * @returns {string} 格式化后的文件大小
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 格式化数字
 * @param {number} num 数字
 * @param {number} decimals 小数位数
 * @returns {string} 格式化后的数字
 */
export const formatNumber = (num, decimals = 0) => {
  if (isNaN(num)) return '0'
  return Number(num).toFixed(decimals)
}

/**
 * 格式化百分比
 * @param {number} value 值
 * @param {number} total 总数
 * @param {number} decimals 小数位数
 * @returns {string} 格式化后的百分比
 */
export const formatPercentage = (value, total, decimals = 1) => {
  if (!total || total === 0) return '0%'
  const percentage = (value / total) * 100
  return formatNumber(percentage, decimals) + '%'
}

/**
 * 截断文本
 * @param {string} text 文本
 * @param {number} length 最大长度
 * @param {string} suffix 后缀
 * @returns {string} 截断后的文本
 */
export const truncateText = (text, length = 50, suffix = '...') => {
  if (!text) return ''
  if (text.length <= length) return text
  return text.substring(0, length) + suffix
}

/**
 * 高亮搜索关键词
 * @param {string} text 文本
 * @param {string} keyword 关键词
 * @returns {string} 高亮后的HTML
 */
export const highlightKeyword = (text, keyword) => {
  if (!text || !keyword) return text
  const regex = new RegExp(`(${keyword})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

/**
 * 格式化考试时长
 * @param {number} minutes 分钟数
 * @returns {string} 格式化后的时长
 */
export const formatDuration = (minutes) => {
  if (!minutes) return '0分钟'
  
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  
  if (hours > 0) {
    return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
  }
  return `${mins}分钟`
}

/**
 * 格式化分数
 * @param {number} score 分数
 * @param {number} total 总分
 * @returns {string} 格式化后的分数
 */
export const formatScore = (score, total) => {
  if (score === null || score === undefined) return '未评分'
  if (total) {
    return `${score}/${total} (${formatPercentage(score, total)}%)`
  }
  return score.toString()
}

/**
 * 格式化状态
 * @param {string} status 状态
 * @returns {object} 状态配置
 */
export const formatStatus = (status) => {
  const statusMap = {
    // 试题状态
    draft: { text: '草稿', type: 'info' },
    published: { text: '已发布', type: 'success' },
    archived: { text: '已归档', type: 'warning' },
    
    // 考试状态
    ongoing: { text: '进行中', type: 'primary' },
    finished: { text: '已结束', type: 'success' },
    exam_cancelled: { text: '已取消', type: 'danger' },
    
    // 用户状态
    active: { text: '正常', type: 'success' },
    inactive: { text: '禁用', type: 'warning' },
    banned: { text: '封禁', type: 'danger' },
    
    // 考试记录状态
    in_progress: { text: '进行中', type: 'primary' },
    submitted: { text: '已提交', type: 'success' },
    timeout: { text: '超时', type: 'warning' },
    record_cancelled: { text: '已取消', type: 'danger' }
  }
  
  return statusMap[status] || { text: status, type: 'default' }
}

/**
 * 格式化题型
 * @param {string} type 题型
 * @returns {object} 题型配置
 */
export const formatQuestionType = (type) => {
  const typeMap = {
    single: { text: '单选题', type: 'primary' },
    multiple: { text: '多选题', type: 'success' },
    judge: { text: '判断题', type: 'warning' },
    fill: { text: '填空题', type: 'info' },
    essay: { text: '简答题', type: 'danger' }
  }
  
  return typeMap[type] || { text: type, type: 'default' }
}

/**
 * 格式化难度
 * @param {string} difficulty 难度
 * @returns {object} 难度配置
 */
export const formatDifficulty = (difficulty) => {
  const difficultyMap = {
    easy: { text: '简单', type: 'success' },
    medium: { text: '中等', type: 'warning' },
    hard: { text: '困难', type: 'danger' }
  }
  
  return difficultyMap[difficulty] || { text: difficulty, type: 'default' }
}

/**
 * 格式化角色
 * @param {string} role 角色
 * @returns {object} 角色配置
 */
export const formatRole = (role) => {
  const roleMap = {
    admin: { text: '管理员', type: 'danger' },
    user: { text: '普通用户', type: 'primary' }
  }
  
  return roleMap[role] || { text: role, type: 'default' }
}

/**
 * 格式化支付方式
 * @param {string} method 支付方式
 * @returns {object} 支付方式配置
 */
export const formatPaymentMethod = (method) => {
  const methodMap = {
    alipay: { text: '支付宝', type: 'primary' },
    wechat: { text: '微信支付', type: 'success' },
    paypal: { text: 'PayPal', type: 'warning' },
    admin: { text: '联系管理员', type: 'info' }
  }
  
  return methodMap[method] || { text: method, type: 'default' }
}

/**
 * 格式化订单状态
 * @param {string} status 订单状态
 * @returns {object} 订单状态配置
 */
export const formatOrderStatus = (status) => {
  const statusMap = {
    pending: { text: '待支付', type: 'warning' },
    paid: { text: '已支付', type: 'success' },
    cancelled: { text: '已取消', type: 'danger' },
    refunded: { text: '已退款', type: 'info' },
    failed: { text: '支付失败', type: 'danger' }
  }
  
  return statusMap[status] || { text: status, type: 'default' }
}

/**
 * 格式化金额
 * @param {number} amount 金额
 * @param {string} currency 货币符号
 * @returns {string} 格式化后的金额
 */
export const formatAmount = (amount, currency = '¥') => {
  if (amount === null || amount === undefined) return '0.00'
  return `${currency}${formatNumber(amount, 2)}`
}

/**
 * 格式化时间范围
 * @param {string|Date} startTime 开始时间
 * @param {string|Date} endTime 结束时间
 * @returns {string} 格式化后的时间范围
 */
export const formatTimeRange = (startTime, endTime) => {
  if (!startTime || !endTime) return ''
  
  const start = dayjs(startTime)
  const end = dayjs(endTime)
  
  if (start.format('YYYY-MM-DD') === end.format('YYYY-MM-DD')) {
    return `${start.format('YYYY-MM-DD')} ${start.format('HH:mm')} - ${end.format('HH:mm')}`
  }
  
  return `${start.format('YYYY-MM-DD HH:mm')} - ${end.format('YYYY-MM-DD HH:mm')}`
}

/**
 * 格式化剩余时间
 * @param {string|Date} endTime 结束时间
 * @returns {string} 格式化后的剩余时间
 */
export const formatRemainingTime = (endTime) => {
  if (!endTime) return ''
  
  const now = dayjs()
  const end = dayjs(endTime)
  
  if (end.isBefore(now)) {
    return '已结束'
  }
  
  const diff = end.diff(now)
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  const seconds = Math.floor((diff % (1000 * 60)) / 1000)
  
  if (hours > 0) {
    return `${hours}小时${minutes}分钟${seconds}秒`
  } else if (minutes > 0) {
    return `${minutes}分钟${seconds}秒`
  } else {
    return `${seconds}秒`
  }
}

/**
 * 格式化考试进度
 * @param {number} current 当前题目
 * @param {number} total 总题目数
 * @returns {string} 格式化后的进度
 */
export const formatProgress = (current, total) => {
  if (!total || total === 0) return '0%'
  return `${current}/${total} (${formatPercentage(current, total)}%)`
}

/**
 * 格式化答题时间
 * @param {number} seconds 秒数
 * @returns {string} 格式化后的答题时间
 */
export const formatAnswerTime = (seconds) => {
  if (!seconds) return '0秒'
  
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}小时${minutes}分钟${secs}秒`
  } else if (minutes > 0) {
    return `${minutes}分钟${secs}秒`
  } else {
    return `${secs}秒`
  }
}

export default {
  formatDate,
  formatRelativeTime,
  formatFileSize,
  formatNumber,
  formatPercentage,
  truncateText,
  highlightKeyword,
  formatDuration,
  formatScore,
  formatStatus,
  formatQuestionType,
  formatDifficulty,
  formatRole,
  formatPaymentMethod,
  formatOrderStatus,
  formatAmount,
  formatTimeRange,
  formatRemainingTime,
  formatProgress,
  formatAnswerTime
}
