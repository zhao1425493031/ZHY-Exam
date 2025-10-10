// 表单验证规则
export const rules = {
  // 必填验证
  required: (message = '此字段为必填项') => ({
    required: true,
    message,
    trigger: 'blur'
  }),
  
  // 邮箱验证
  email: () => ({
    type: 'email',
    message: '请输入正确的邮箱地址',
    trigger: 'blur'
  }),
  
  // 手机号验证
  phone: () => ({
    pattern: /^1[3-9]\d{9}$/,
    message: '请输入正确的手机号码',
    trigger: 'blur'
  }),
  
  // 用户名验证
  username: () => ({
    pattern: /^[a-zA-Z0-9_]{3,20}$/,
    message: '用户名只能包含字母、数字、下划线，长度3-20位',
    trigger: 'blur'
  }),
  
  // 密码验证
  password: () => ({
    min: 6,
    max: 20,
    message: '密码长度应为6-20位',
    trigger: 'blur'
  }),
  
  // 确认密码验证
  confirmPassword: (password) => ({
    validator: (rule, value, callback) => {
      if (value !== password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    },
    trigger: 'blur'
  }),
  
  // 长度验证
  minLength: (min, message) => ({
    min,
    message: message || `长度不能少于${min}个字符`,
    trigger: 'blur'
  }),
  
  maxLength: (max, message) => ({
    max,
    message: message || `长度不能超过${max}个字符`,
    trigger: 'blur'
  }),
  
  // 数字验证
  number: () => ({
    type: 'number',
    message: '请输入数字',
    trigger: 'blur'
  }),
  
  // 整数验证
  integer: () => ({
    pattern: /^\d+$/,
    message: '请输入正整数',
    trigger: 'blur'
  }),
  
  // URL验证
  url: () => ({
    type: 'url',
    message: '请输入正确的URL地址',
    trigger: 'blur'
  }),
  
  // 正则表达式验证
  pattern: (pattern, message) => ({
    pattern,
    message,
    trigger: 'blur'
  })
}

// 常用验证规则组合
export const commonRules = {
  // 用户名规则
  username: [
    rules.required('请输入用户名'),
    rules.username()
  ],
  
  // 邮箱规则
  email: [
    rules.required('请输入邮箱'),
    rules.email()
  ],
  
  // 手机号规则
  phone: [
    rules.required('请输入手机号'),
    rules.phone()
  ],
  
  // 密码规则
  password: [
    rules.required('请输入密码'),
    rules.password()
  ],
  
  // 姓名规则
  realName: [
    rules.required('请输入姓名'),
    rules.minLength(2, '姓名至少2个字符'),
    rules.maxLength(20, '姓名不能超过20个字符')
  ],
  
  // 科目名称规则
  subjectName: [
    rules.required('请输入科目名称'),
    rules.minLength(2, '科目名称至少2个字符'),
    rules.maxLength(50, '科目名称不能超过50个字符')
  ],
  
  // 科目代码规则
  subjectCode: [
    rules.required('请输入科目代码'),
    rules.pattern(/^[A-Z0-9_]{2,20}$/, '科目代码只能包含大写字母、数字、下划线，长度2-20位')
  ],
  
  // 试题标题规则
  questionTitle: [
    rules.required('请输入试题标题'),
    rules.minLength(5, '试题标题至少5个字符'),
    rules.maxLength(500, '试题标题不能超过500个字符')
  ],
  
  // 考试标题规则
  examTitle: [
    rules.required('请输入考试标题'),
    rules.minLength(5, '考试标题至少5个字符'),
    rules.maxLength(100, '考试标题不能超过100个字符')
  ],
  
  // 考试时长规则
  examDuration: [
    rules.required('请输入考试时长'),
    rules.integer(),
    {
      validator: (rule, value, callback) => {
        if (value < 5) {
          callback(new Error('考试时长不能少于5分钟'))
        } else if (value > 300) {
          callback(new Error('考试时长不能超过300分钟'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

