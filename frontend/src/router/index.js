import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 路由配置
const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { 
      title: '登录',
      requiresAuth: false 
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { 
      title: '注册',
      requiresAuth: false 
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
    name: 'Admin',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { 
      title: '管理后台',
      requiresAuth: true,
      requiresRole: ['admin']
    },
    children: [
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('@/views/admin/UserManagement.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'subjects',
        name: 'SubjectManagement',
        component: () => import('@/views/admin/SubjectManagement.vue'),
        meta: { title: '科目管理' }
      },
      {
        path: 'questions',
        name: 'QuestionManagement',
        component: () => import('@/views/admin/QuestionManagement.vue'),
        meta: { title: '试题管理' }
      },
      {
        path: 'exams',
        name: 'ExamManagement',
        component: () => import('@/views/admin/ExamManagement.vue'),
        meta: { title: '考试管理' }
      },
      {
        path: 'question-bank',
        name: 'QuestionBank',
        component: () => import('@/views/admin/QuestionBank.vue'),
        meta: { title: '题库管理' }
      },
      {
        path: 'exam-creation',
        name: 'ExamCreation',
        component: () => import('@/views/admin/ExamCreation.vue'),
        meta: { title: '创建考试' }
      },
      {
        path: 'exam-analysis',
        name: 'ExamAnalysis',
        component: () => import('@/views/admin/ExamAnalysis.vue'),
        meta: { title: '考试分析' }
      }
    ]
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { 
      title: '用户中心',
      requiresAuth: true,
      requiresRole: ['admin', 'user']
    },
    children: [
      {
        path: 'exam-list',
        name: 'ExamList',
        component: () => import('@/views/user/ExamList.vue'),
        meta: { title: '考试列表' }
      },
      {
        path: 'exam-taking/:id',
        name: 'ExamTaking',
        component: () => import('@/views/user/ExamTaking.vue'),
        meta: { title: '在线考试' }
      },
      {
        path: 'exam-result/:id',
        name: 'ExamResult',
        component: () => import('@/views/user/ExamResult.vue'),
        meta: { title: '考试结果' }
      },
      {
        path: 'my-records',
        name: 'MyRecords',
        component: () => import('@/views/user/MyRecords.vue'),
        meta: { title: '我的记录' }
      }
    ]
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
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - ExamSphere`
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // 检查角色权限
  if (to.meta.requiresRole && !to.meta.requiresRole.includes(authStore.userRole)) {
    next('/dashboard')
    return
  }
  
  // 已登录用户访问登录页面，重定向到仪表盘
  if ((to.path === '/login' || to.path === '/register') && authStore.isLoggedIn) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router
