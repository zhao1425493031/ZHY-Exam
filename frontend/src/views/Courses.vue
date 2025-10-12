<template>
  <div class="courses-page">
    <!-- 顶部导航栏 -->
    <TopNavigation />

    <!-- 课程列表内容 -->
    <div class="courses-content">
      <div class="container">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item>
            <router-link to="/">首页</router-link>
          </el-breadcrumb-item>
          <el-breadcrumb-item>课程</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 页面标题和筛选 -->
        <div class="page-header">
          <div class="header-content">
            <h1>课程中心</h1>
            <p>发现优质课程，提升你的技能</p>
          </div>
          
          <div class="filters-section">
            <!-- 搜索框 -->
            <div class="search-box">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索课程..."
                @input="handleSearch"
                clearable
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>

            <!-- 筛选条件 -->
            <div class="filter-tabs">
              <el-button 
                v-for="category in courseCategories" 
                :key="category.value"
                :type="selectedCategory === category.value ? 'primary' : ''"
                @click="filterCourses(category.value)"
                size="small"
              >
                {{ category.label }}
              </el-button>
            </div>

            <!-- 排序选项 -->
            <div class="sort-options">
              <el-select v-model="sortBy" @change="handleSort" placeholder="排序方式">
                <el-option label="最新发布" value="newest" />
                <el-option label="最受欢迎" value="popular" />
                <el-option label="评分最高" value="rating" />
                <el-option label="价格从低到高" value="price_asc" />
                <el-option label="价格从高到低" value="price_desc" />
              </el-select>
            </div>
          </div>
        </div>

        <!-- 课程统计 -->
        <div class="courses-stats">
          <div class="stat-item">
            <span class="stat-number">{{ totalCourses }}</span>
            <span class="stat-label">总课程数</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ freeCoursesCount }}</span>
            <span class="stat-label">免费课程</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ paidCoursesCount }}</span>
            <span class="stat-label">付费课程</span>
          </div>
        </div>

        <!-- 课程列表 -->
        <div class="courses-list" v-loading="loading">
          <div class="courses-grid">
            <div 
              v-for="course in paginatedCourses" 
              :key="course.id"
              class="course-card"
              @click="viewCourse(course)"
            >
              <div class="course-image">
                <img :src="course.image || '/default-course.svg'" :alt="course.name">
                <div class="course-overlay">
                  <el-button type="primary" size="small" @click.stop="viewCourse(course)">
                    查看详情
                  </el-button>
                </div>
                <div class="course-badge" v-if="course.is_free">
                  <span>免费</span>
                </div>
                <div class="course-badge price" v-else>
                  <span>¥{{ course.price }}</span>
                </div>
              </div>
              
              <div class="course-content">
                <h3>{{ course.name }}</h3>
                <p class="course-description">{{ course.description }}</p>
                
                <div class="course-meta">
                  <div class="course-category">
                    <el-icon><Folder /></el-icon>
                    <span>{{ course.category || '未分类' }}</span>
                  </div>
                  <div class="course-stats">
                    <span class="course-students">
                      <el-icon><User /></el-icon>
                      {{ course.student_count || 0 }}人学习
                    </span>
                    <span class="course-rating">
                      <el-icon><Star /></el-icon>
                      {{ course.rating || 4.8 }}
                    </span>
                  </div>
                </div>

                <div class="course-footer">
                  <div class="course-instructor">
                    <el-avatar :size="24" :src="course.instructor_avatar">
                      {{ course.instructor_name?.charAt(0) || 'A' }}
                    </el-avatar>
                    <span>{{ course.instructor_name || '讲师' }}</span>
                  </div>
                  <div class="course-duration">
                    <el-icon><Clock /></el-icon>
                    <span>{{ course.duration || '2小时' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="filteredCourses.length === 0 && !loading" class="empty-state">
            <el-empty description="暂无课程" :image-size="120">
              <el-button type="primary" @click="resetFilters">重置筛选</el-button>
            </el-empty>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper" v-if="filteredCourses.length > 0">
          <el-pagination
            :current-page="currentPage"
            :page-size="pageSize"
            :page-sizes="[12, 24, 48, 96]"
            :total="filteredCourses.length"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Search, Folder, User, Star, Clock 
} from '@element-plus/icons-vue'
import TopNavigation from '@/components/layout/TopNavigation.vue'
import { subjectsApi } from '@/api/subjects'

export default {
  name: 'Courses',
  components: {
    TopNavigation,
    Search,
    Folder,
    User,
    Star,
    Clock
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const loading = ref(false)
    const courses = ref([])
    const searchKeyword = ref('')
    const selectedCategory = ref('all')
    const sortBy = ref('newest')
    const currentPage = ref(1)
    const pageSize = ref(12)

    // 课程分类
    const courseCategories = ref([
      { label: '全部', value: 'all' },
      { label: '免费课程', value: 'free' },
      { label: '付费课程', value: 'paid' },
      { label: '编程开发', value: 'programming' },
      { label: '设计创意', value: 'design' },
      { label: '商业管理', value: 'business' },
      { label: '语言学习', value: 'language' },
      { label: '职业技能', value: 'skill' }
    ])

    // 过滤后的课程
    const filteredCourses = computed(() => {
      let result = courses.value

      // 按分类过滤
      if (selectedCategory.value !== 'all') {
        switch (selectedCategory.value) {
          case 'free':
            result = result.filter(course => course.is_free)
            break
          case 'paid':
            result = result.filter(course => !course.is_free)
            break
          default:
            result = result.filter(course => course.category === selectedCategory.value)
        }
      }

      // 按关键词搜索
      if (searchKeyword.value) {
        const keyword = searchKeyword.value.toLowerCase()
        result = result.filter(course => 
          course.name.toLowerCase().includes(keyword) ||
          course.description.toLowerCase().includes(keyword) ||
          (course.category && course.category.toLowerCase().includes(keyword))
        )
      }

      // 排序
      switch (sortBy.value) {
        case 'newest':
          result = result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          break
        case 'popular':
          result = result.sort((a, b) => (b.student_count || 0) - (a.student_count || 0))
          break
        case 'rating':
          result = result.sort((a, b) => (b.rating || 0) - (a.rating || 0))
          break
        case 'price_asc':
          result = result.sort((a, b) => (a.price || 0) - (b.price || 0))
          break
        case 'price_desc':
          result = result.sort((a, b) => (b.price || 0) - (a.price || 0))
          break
      }

      return result
    })

    // 分页后的课程
    const paginatedCourses = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredCourses.value.slice(start, end)
    })

    // 统计信息
    const totalCourses = computed(() => courses.value.length)
    const freeCoursesCount = computed(() => courses.value.filter(course => course.is_free).length)
    const paidCoursesCount = computed(() => courses.value.filter(course => !course.is_free).length)

    // 获取课程列表
    const fetchCourses = async () => {
      try {
        loading.value = true
        const response = await subjectsApi.getSubjects({
          status: 'active',
          page: 1,
          size: 100 // 获取更多课程用于前端筛选
        })
        
        // 为课程添加模拟数据
        courses.value = (response.data.items || []).map(course => ({
          ...course,
          student_count: Math.floor(Math.random() * 1000) + 100,
          rating: (Math.random() * 1 + 4).toFixed(1),
          instructor_name: '张老师',
          instructor_avatar: '',
          duration: `${Math.floor(Math.random() * 5) + 1}小时`,
          image: course.cover_image || '/default-course.svg',
          created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
        }))
      } catch (error) {
        console.error('获取课程列表失败:', error)
        ElMessage.error('获取课程列表失败')
      } finally {
        loading.value = false
      }
    }

    // 过滤课程
    const filterCourses = (category) => {
      selectedCategory.value = category
      currentPage.value = 1
    }

    // 搜索处理
    const handleSearch = () => {
      currentPage.value = 1
    }

    // 排序处理
    const handleSort = () => {
      currentPage.value = 1
    }

    // 重置筛选
    const resetFilters = () => {
      searchKeyword.value = ''
      selectedCategory.value = 'all'
      sortBy.value = 'newest'
      currentPage.value = 1
    }

    // 分页处理
    const handlePageChange = (page) => {
      currentPage.value = page
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }

    // 查看课程
    const viewCourse = (course) => {
      router.push(`/course/${course.id}`)
    }

    // 监听路由参数
    watch(() => route.query, (newQuery) => {
      if (newQuery.type) {
        selectedCategory.value = newQuery.type
      }
      if (newQuery.category) {
        selectedCategory.value = newQuery.category
      }
    }, { immediate: true })

    onMounted(() => {
      fetchCourses()
    })

    return {
      loading,
      courses,
      searchKeyword,
      selectedCategory,
      sortBy,
      currentPage,
      pageSize,
      courseCategories,
      filteredCourses,
      paginatedCourses,
      totalCourses,
      freeCoursesCount,
      paidCoursesCount,
      filterCourses,
      handleSearch,
      handleSort,
      resetFilters,
      handlePageChange,
      handleSizeChange,
      viewCourse
    }
  }
}
</script>

<style lang="scss" scoped>
.courses-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  padding: 20px 0;
  
  :deep(.el-breadcrumb__item) {
    .el-breadcrumb__inner {
      color: #666;
      
      &:hover {
        color: #667eea;
      }
    }
    
    &:last-child .el-breadcrumb__inner {
      color: #333;
    }
  }
}

.courses-content {
  padding-bottom: 4rem;
}

.page-header {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

  .header-content {
    text-align: center;
    margin-bottom: 2rem;

    h1 {
      font-size: 2.5rem;
      font-weight: bold;
      margin-bottom: 0.5rem;
      color: #333;
    }

    p {
      font-size: 1.1rem;
      color: #666;
    }
  }

  .filters-section {
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 1rem;
    align-items: center;

    .search-box {
      max-width: 400px;
    }

    .filter-tabs {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .sort-options {
      min-width: 150px;
    }
  }
}

.courses-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;

  .stat-item {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    .stat-number {
      display: block;
      font-size: 2rem;
      font-weight: bold;
      color: #667eea;
      margin-bottom: 0.5rem;
    }

    .stat-label {
      font-size: 0.9rem;
      color: #666;
    }
  }
}

.courses-list {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .course-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;

    &:hover {
      transform: translateY(-8px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);

      .course-overlay {
        opacity: 1;
      }
    }

    .course-image {
      position: relative;
      height: 180px;
      overflow: hidden;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
      }

      .course-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
      }

      .course-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        z-index: 2;

        &.price {
          background: linear-gradient(135deg, #ff6b6b, #ee5a52);
          color: white;
        }

        &:not(.price) {
          background: linear-gradient(135deg, #4ecdc4, #44a08d);
          color: white;
        }
      }
    }

    .course-content {
      padding: 1.5rem;

      h3 {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
        color: #333;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .course-description {
        color: #666;
        margin-bottom: 1rem;
        line-height: 1.5;
        font-size: 0.9rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .course-meta {
        margin-bottom: 1rem;

        .course-category {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.8rem;
          font-size: 0.9rem;
          color: #667eea;
          font-weight: 500;
        }

        .course-stats {
          display: flex;
          justify-content: space-between;
          font-size: 0.85rem;
          color: #999;

          .course-students,
          .course-rating {
            display: flex;
            align-items: center;
            gap: 0.3rem;
          }
        }
      }

      .course-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid #f0f0f0;

        .course-instructor {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          color: #666;
        }

        .course-duration {
          display: flex;
          align-items: center;
          gap: 0.3rem;
          font-size: 0.85rem;
          color: #999;
        }
      }
    }
  }

  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

// 响应式设计
@media (max-width: 768px) {
  .page-header .filters-section {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .courses-stats {
    grid-template-columns: 1fr;
  }

  .courses-list .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>
