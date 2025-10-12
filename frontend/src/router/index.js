import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { 
      title: '首页',
      requiresAuth: false 
    }
  },
  {
    path: '/courses',
    name: 'Courses',
    component: () => import('@/views/Courses.vue'),
    meta: { 
      title: '课程列表',
      requiresAuth: false
    }
  },
  {
    path: '/course/:id',
    name: 'CourseDetail',
    component: () => import('@/views/CourseDetail.vue'),
    meta: { 
      title: '课程详情',
      requiresAuth: false
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue'),
    meta: { 
      title: '关于我们',
      requiresAuth: false 
    }
  },
  {
    path: '/exam/detail/:id',
    name: 'ExamDetail',
    component: () => import('@/views/ExamDetail.vue'),
    meta: { 
      title: '考试详情',
      requiresAuth: false 
    }
  },
  {
    path: '/exam/:id',
    name: 'PublicExamTaking',
    component: () => import('@/views/ExamTaking.vue'),
    meta: { 
      title: '在线考试',
      requiresAuth: false 
    }
  },
  {
    path: '/exam/result/:id',
    name: 'PublicExamResult',
    component: () => import('@/views/ExamResult.vue'),
    meta: { 
      title: '考试结果',
      requiresAuth: true 
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { 
      title: '仪表盘',
      requiresAuth: true 
    },
    children: [
      {
        path: '',
        name: 'DashboardHome',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘' }
      }
    ]
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('@/views/admin/AdminDashboard.vue'),
    meta: { 
      title: '管理员控制台',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  // 独立的管理页面路由
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: () => import('@/views/admin/UserManagement.vue'),
    meta: { 
      title: '用户管理',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/subjects',
    name: 'SubjectManagement',
    component: () => import('@/views/admin/SubjectManagement.vue'),
    meta: { 
      title: '科目管理',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/questions',
    name: 'QuestionManagement',
    component: () => import('@/views/admin/QuestionManagement.vue'),
    meta: { 
      title: '试题管理',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/exams',
    name: 'ExamManagement',
    component: () => import('@/views/admin/ExamManagement.vue'),
    meta: { 
      title: '考试管理',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/question-bank',
    name: 'QuestionBank',
    component: () => import('@/views/admin/QuestionBank.vue'),
    meta: { 
      title: '题库管理',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/exam-creation',
    name: 'ExamCreation',
    component: () => import('@/views/admin/ExamCreation.vue'),
    meta: { 
      title: '创建考试',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/exam-analysis',
    name: 'ExamAnalysis',
    component: () => import('@/views/admin/ExamAnalysis.vue'),
    meta: { 
      title: '考试分析',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/permissions',
    name: 'PermissionManagement',
    component: () => import('@/views/admin/PermissionManagement.vue'),
    meta: { 
      title: '权限管理',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/import-export',
    name: 'ImportExportManagement',
    component: () => import('@/views/admin/ImportExportManagement.vue'),
    meta: { 
      title: '数据导入导出',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  {
    path: '/admin/statistics',
    name: 'StatisticsAnalysis',
    component: () => import('@/views/admin/StatisticsAnalysis.vue'),
    meta: { 
      title: '统计分析',
      requiresAuth: true,
      requiresRole: ['admin']
    }
  },
  // 用户仪表盘 - 独立路由，不包含旧的导航栏
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: () => import('@/views/user/UserDashboard.vue'),
    meta: { 
      title: '我的仪表盘',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  // 用户相关页面 - 全部独立路由，不包含旧的导航栏
  {
    path: '/user/exam-list',
    name: 'ExamList',
    component: () => import('@/views/user/ExamList.vue'),
    meta: { 
      title: '考试列表',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/exam-taking/:id',
    name: 'ExamTaking',
    component: () => import('@/views/user/ExamTaking.vue'),
    meta: { 
      title: '在线考试',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/exam-result/:id',
    name: 'ExamResult',
    component: () => import('@/views/user/ExamResult.vue'),
    meta: { 
      title: '考试结果',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/my-records',
    name: 'MyRecords',
    component: () => import('@/views/user/MyRecords.vue'),
    meta: { 
      title: '我的记录',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/wrong-answers',
    name: 'WrongAnswers',
    component: () => import('@/views/user/WrongAnswers.vue'),
    meta: { 
      title: '错题管理',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/learning-progress',
    name: 'LearningProgress',
    component: () => import('@/views/user/LearningProgress.vue'),
    meta: { 
      title: '学习进度',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/notifications',
    name: 'Notifications',
    component: () => import('@/views/user/Notifications.vue'),
    meta: { 
      title: '消息通知',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/file-management',
    name: 'FileManagement',
    component: () => import('@/views/user/FileManagement.vue'),
    meta: { 
      title: '文件管理',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/user/announcements',
    name: 'AnnouncementManagement',
    component: () => import('@/views/user/AnnouncementManagement.vue'),
    meta: { 
      title: '系统公告',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - ExamSphere`
  }
  
  // 如果有token但没有用户信息，尝试恢复用户状态
  if (authStore.token && !authStore.user) {
    try {
      await authStore.initUser()
    } catch (error) {
      console.error('恢复用户状态失败:', error)
    }
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 显示登录弹窗而不是跳转到登录页
    authStore.openLoginDialog()
    ElMessage.warning('请先登录')
    next(false) // 取消导航
    return
  }
  
  // 检查角色权限
  if (to.meta.requiresRole && !to.meta.requiresRole.includes(authStore.userRole)) {
    ElMessage.error('权限不足')
    next(from.path || '/')
    return
  }
  
  next()
})

export default router
