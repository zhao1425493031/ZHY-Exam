<template>
  <div class="modern-exam-creation">
    <!-- 现代化头部 -->
    <div class="modern-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-title">
            <div class="title-icon">
              <el-icon><EditPen /></el-icon>
            </div>
            <div class="title-text">
              <h1>{{ isEditMode ? '考试编辑' : '考试创建' }}</h1>
              <p>{{ isEditMode ? '编辑考试并重新组卷配置' : '创建新考试并组卷配置' }}</p>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-button @click="$router.push('/admin/exams')" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回列表</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 步骤条 -->
    <div class="steps-section">
      <div class="steps-container">
        <el-steps :active="currentStep" finish-status="success" align-center>
          <el-step title="基本信息" description="配置考试基本信息" />
          <el-step title="选择试题" description="手动选题或随机组卷" />
          <el-step title="考试设置" description="配置考试规则" />
          <el-step title="预览确认" :description="isEditMode ? '预览并更新考试' : '预览并创建考试'" />
        </el-steps>
      </div>
    </div>

    <!-- 表单区域 -->
    <div class="form-section">
      <div class="form-card">
        <!-- 步骤1: 基本信息 -->
        <div v-show="currentStep === 0" class="step-content">
          <h3 class="step-title">考试基本信息</h3>
          <el-form :model="examForm" :rules="basicRules" ref="basicFormRef" label-width="120px">
        <el-form-item label="考试标题" prop="title">
              <el-input v-model="examForm.title" placeholder="请输入考试标题" />
        </el-form-item>
        <el-form-item label="考试描述" prop="description">
          <el-input
                v-model="examForm.description"
            type="textarea"
                :rows="4"
            placeholder="请输入考试描述"
          />
        </el-form-item>
            <el-form-item label="选择科目" prop="subject_id">
              <el-select
                v-model="examForm.subject_id"
                placeholder="请选择科目"
                style="width: 100%"
                @change="handleSubjectChange"
              >
            <el-option
              v-for="subject in subjects"
              :key="subject.id"
              :label="subject.name"
              :value="subject.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="考试时长" prop="duration">
              <el-input-number v-model="examForm.duration" :min="1" :max="300" /> 分钟
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
                v-model="examForm.start_time"
            type="datetime"
            placeholder="选择开始时间"
                style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
                v-model="examForm.end_time"
            type="datetime"
            placeholder="选择结束时间"
                style="width: 100%"
          />
        </el-form-item>
          </el-form>
        </div>
        
        <!-- 步骤2: 选择试题 -->
        <div v-show="currentStep === 1" class="step-content">
          <h3 class="step-title">选择试题</h3>
          
          <el-tabs v-model="questionSelectMode" class="question-tabs">
            <el-tab-pane label="手动选题" name="manual">
              <div class="manual-selection">
                <div class="search-bar">
                  <el-input
                    v-model="questionSearch"
                    placeholder="搜索试题"
                    prefix-icon="Search"
                    clearable
                  />
                  <el-select v-model="questionType" placeholder="题型" clearable style="width: 150px; margin-left: 12px;">
                    <el-option label="单选题" value="single" />
                    <el-option label="多选题" value="multiple" />
                    <el-option label="判断题" value="judge" />
                    <el-option label="填空题" value="fill" />
                    <el-option label="简答题" value="essay" />
                  </el-select>
                  <el-select v-model="questionDifficulty" placeholder="难度" clearable style="width: 120px; margin-left: 12px;">
                    <el-option label="简单" value="easy" />
                    <el-option label="中等" value="medium" />
                    <el-option label="困难" value="hard" />
                  </el-select>
                  <el-button type="primary" @click="searchQuestions" style="margin-left: 12px;">搜索</el-button>
                </div>
                
                <div class="question-list">
                  <el-table
                    :data="availableQuestions"
                    @selection-change="handleQuestionSelect"
                    row-key="id"
                    max-height="400"
                    :loading="loadingQuestions"
                  >
                    <el-table-column type="selection" width="55" />
                    <el-table-column prop="id" label="ID" width="80" />
                    <el-table-column prop="title" label="题目" min-width="200" show-overflow-tooltip />
                    <el-table-column prop="type" label="题型" width="100">
                      <template #default="{ row }">
                        {{ getTypeLabel(row.type) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="difficulty" label="难度" width="100">
                      <template #default="{ row }">
                        {{ getDifficultyLabel(row.difficulty) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="points" label="分值" width="80" />
                  </el-table>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="随机组卷" name="random">
              <div class="random-selection">
                <el-form :model="randomForm" label-width="120px">
                  <el-form-item label="单选题数量">
                    <el-input-number v-model="randomForm.single" :min="0" :max="50" />
                  </el-form-item>
                  <el-form-item label="多选题数量">
                    <el-input-number v-model="randomForm.multiple" :min="0" :max="50" />
                  </el-form-item>
                  <el-form-item label="判断题数量">
                    <el-input-number v-model="randomForm.judge" :min="0" :max="50" />
                  </el-form-item>
                  <el-form-item label="填空题数量">
                    <el-input-number v-model="randomForm.fill" :min="0" :max="50" />
                </el-form-item>
                  <el-form-item label="简答题数量">
                    <el-input-number v-model="randomForm.essay" :min="0" :max="50" />
                </el-form-item>
                  <el-form-item label="难度分布">
                    <el-radio-group v-model="randomForm.difficulty_mode">
                      <el-radio value="random">随机</el-radio>
                      <el-radio value="easy">简单为主</el-radio>
                      <el-radio value="medium">中等为主</el-radio>
                      <el-radio value="hard">困难为主</el-radio>
                    </el-radio-group>
                </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="generateRandomQuestions">生成试题</el-button>
          </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
          </el-tabs>
          
          <div class="selected-questions">
            <h4>已选试题（{{ selectedQuestions.length }}题，共{{ totalPoints }}分）</h4>
            <div class="selected-list">
              <el-tag
                v-for="(question, index) in selectedQuestions"
                :key="question.id"
                closable
                @close="removeQuestion(index)"
                style="margin: 4px;"
              >
                {{ index + 1 }}. {{ question.title.substring(0, 30) }}...（{{ question.points }}分）
              </el-tag>
            </div>
          </div>
        </div>
        
        <!-- 步骤3: 考试设置 -->
        <div v-show="currentStep === 2" class="step-content">
          <h3 class="step-title">考试设置</h3>
          <el-form :model="settingsForm" label-width="160px">
            <el-form-item label="打乱题目顺序">
              <el-switch v-model="settingsForm.shuffle_questions" />
            </el-form-item>
            <el-form-item label="打乱选项顺序">
              <el-switch v-model="settingsForm.shuffle_options" />
            </el-form-item>
            <el-form-item label="显示答案">
              <el-switch v-model="settingsForm.show_answer" />
            </el-form-item>
            <el-form-item label="显示解析">
              <el-switch v-model="settingsForm.show_explanation" />
            </el-form-item>
            <el-form-item label="允许重考">
              <el-switch v-model="settingsForm.allow_retake" />
            </el-form-item>
            <el-form-item label="合格分数" prop="passing_score">
              <el-input-number 
                v-model="examForm.passing_score" 
                :min="0" 
                :max="totalPoints" 
                placeholder="请输入合格分数"
              />
              <span class="form-tip">（默认{{ Math.floor(totalPoints * 0.6) }}分，即60%）</span>
            </el-form-item>
            <el-form-item label="考试状态">
              <el-radio-group v-model="examForm.status">
                <el-radio value="draft">保存为草稿</el-radio>
                <el-radio value="published">直接发布</el-radio>
              </el-radio-group>
          </el-form-item>
          </el-form>
        </div>
        
        <!-- 步骤4: 预览确认 -->
        <div v-show="currentStep === 3" class="step-content">
          <h3 class="step-title">预览确认</h3>
          <div class="preview-content">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="考试标题">{{ examForm.title }}</el-descriptions-item>
              <el-descriptions-item label="科目">{{ getSubjectName(examForm.subject_id) }}</el-descriptions-item>
              <el-descriptions-item label="考试时长">{{ examForm.duration }} 分钟</el-descriptions-item>
              <el-descriptions-item label="题目数量">{{ selectedQuestions.length }} 题</el-descriptions-item>
              <el-descriptions-item label="总分">{{ totalPoints }} 分</el-descriptions-item>
              <el-descriptions-item label="合格分数">{{ examForm.passing_score || Math.floor(totalPoints * 0.6) }} 分</el-descriptions-item>
              <el-descriptions-item label="开始时间">{{ formatDate(examForm.start_time) || '未设置' }}</el-descriptions-item>
              <el-descriptions-item label="结束时间">{{ formatDate(examForm.end_time) || '未设置' }}</el-descriptions-item>
              <el-descriptions-item label="考试状态">
                <el-tag :type="examForm.status === 'published' ? 'success' : 'info'">
                  {{ examForm.status === 'published' ? '已发布' : '草稿' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="考试描述" :span="2">
                {{ examForm.description || '无描述' }}
              </el-descriptions-item>
            </el-descriptions>
            
            <div class="question-preview" style="margin-top: 24px;">
              <h4>试题列表</h4>
              <el-table :data="selectedQuestions" border max-height="300">
                <el-table-column type="index" label="序号" width="80" />
                <el-table-column prop="title" label="题目" min-width="200" show-overflow-tooltip />
                <el-table-column prop="type" label="题型" width="100">
                  <template #default="{ row }">
                    {{ getTypeLabel(row.type) }}
                  </template>
                </el-table-column>
                <el-table-column prop="difficulty" label="难度" width="100">
                  <template #default="{ row }">
                    {{ getDifficultyLabel(row.difficulty) }}
                  </template>
                </el-table-column>
                <el-table-column prop="points" label="分值" width="80" />
              </el-table>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="form-actions">
          <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
          <el-button v-if="currentStep < 3" type="primary" @click="nextStep">下一步</el-button>
          <el-button v-if="currentStep === 3" type="success" @click="submitExam" :loading="submitting">
            {{ isEditMode ? '更新考试' : '创建考试' }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  ArrowLeft, EditPen
} from '@element-plus/icons-vue'
import { examApi } from '@/api/exams'
import { subjectsApi } from '@/api/subjects'
import { questionApi } from '@/api/questions'

export default {
  name: 'ExamCreation',
  components: {
    ArrowLeft,
    EditPen
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const currentStep = ref(0)
    const submitting = ref(false)
    
    // 检查是否为编辑模式
    const isEditMode = computed(() => route.query.mode === 'edit')
    const examId = computed(() => route.query.examId ? parseInt(route.query.examId) : null)
    const subjects = ref([])
    const availableQuestions = ref([])
    const selectedQuestions = ref([])
    const questionSelectMode = ref('manual')
    const questionSearch = ref('')
    const questionType = ref('')
    const questionDifficulty = ref('')
    const basicFormRef = ref(null)
    const loadingQuestions = ref(false)
    
    const examForm = reactive({
      title: '',
      description: '',
      subject_id: '',
      duration: 60,
      passing_score: null, // 合格分数
      start_time: null,
      end_time: null,
      status: 'draft'
    })
    
    const randomForm = reactive({
      single: 0,
      multiple: 0,
      judge: 0,
      fill: 0,
      essay: 0,
      difficulty_mode: 'random'
    })
    
    const settingsForm = reactive({
      shuffle_questions: false,
      shuffle_options: false,
      show_answer: true,
      show_explanation: true,
      allow_retake: false
    })
    
    const basicRules = {
      title: [{ required: true, message: '请输入考试标题', trigger: 'blur' }],
      subject_id: [{ required: true, message: '请选择科目', trigger: 'change' }],
      duration: [{ required: true, message: '请输入考试时长', trigger: 'blur' }]
    }
    
    const totalPoints = computed(() => {
      return selectedQuestions.value.reduce((sum, q) => sum + (q.points || 0), 0)
    })
    
    const loadSubjects = async () => {
      try {
        const response = await subjectsApi.getSubjects()
        subjects.value = response.data.items || response.data
      } catch (error) {
        console.error('Load subjects error:', error)
      }
    }
    
    const handleSubjectChange = async () => {
      if (examForm.subject_id) {
        // 清空之前的搜索结果
        availableQuestions.value = []
        selectedQuestions.value = []
        // 自动加载该科目的试题
        await searchQuestions()
      }
    }
    
    const searchQuestions = async () => {
      if (!examForm.subject_id) {
        ElMessage.warning('请先选择科目')
        return
      }
      
      loadingQuestions.value = true
      try {
        const params = {
          subject_id: examForm.subject_id
          // 暂时不限制状态，看看所有试题
        }
        if (questionSearch.value) params.keyword = questionSearch.value
        if (questionType.value) params.type = questionType.value
        if (questionDifficulty.value) params.difficulty = questionDifficulty.value
        
        console.log('搜索试题参数:', params)
        const response = await questionApi.getQuestions(params)
        console.log('试题搜索响应:', response)
        
        availableQuestions.value = response.data.items || response.data || []
        console.log('可用试题数量:', availableQuestions.value.length)
        
        if (availableQuestions.value.length === 0) {
          ElMessage.info('该科目暂无试题')
        } else {
          ElMessage.success(`找到 ${availableQuestions.value.length} 道试题`)
        }
      } catch (error) {
        ElMessage.error('加载试题失败')
        console.error('Search questions error:', error)
      } finally {
        loadingQuestions.value = false
      }
    }
    
    const handleQuestionSelect = (selection) => {
      selectedQuestions.value = [...new Set([...selectedQuestions.value, ...selection])]
    }
    
    const removeQuestion = (index) => {
      selectedQuestions.value.splice(index, 1)
    }
    
    const generateRandomQuestions = async () => {
      if (!examForm.subject_id) {
        ElMessage.warning('请先选择科目')
        return
      }
      
      const total = randomForm.single + randomForm.multiple + randomForm.judge + 
                   randomForm.fill + randomForm.essay
      
      if (total === 0) {
        ElMessage.warning('请至少设置一种题型的数量')
        return
      }
      
      try {
        const response = await questionApi.getQuestions({
          subject_id: examForm.subject_id,
          status: 'published'
        })
        const allQuestions = response.data.items || response.data
        
        selectedQuestions.value = []
        
        // 按题型随机选择
        const types = ['single', 'multiple', 'judge', 'fill', 'essay']
        types.forEach(type => {
          const count = randomForm[type]
          if (count > 0) {
            const typeQuestions = allQuestions.filter(q => q.type === type)
            const shuffled = typeQuestions.sort(() => 0.5 - Math.random())
            selectedQuestions.value.push(...shuffled.slice(0, count))
          }
        })
        
        ElMessage.success(`成功生成${selectedQuestions.value.length}道试题`)
      } catch (error) {
        ElMessage.error('生成试题失败')
        console.error('Generate questions error:', error)
      }
    }
    
    const nextStep = async () => {
      if (currentStep.value === 0) {
        try {
          await basicFormRef.value.validate()
          currentStep.value++
        } catch (error) {
          ElMessage.warning('请完善基本信息')
        }
      } else if (currentStep.value === 1) {
        if (selectedQuestions.value.length === 0) {
          ElMessage.warning('请至少选择一道试题')
          return
        }
        currentStep.value++
      } else {
        currentStep.value++
      }
    }
    
    const prevStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }
    
    const submitExam = async () => {
      try {
        submitting.value = true
        
        // 计算合格分数：如果未设置则使用默认60%
        const passingScore = examForm.passing_score !== null && examForm.passing_score !== undefined
          ? examForm.passing_score
          : Math.floor(totalPoints.value * 0.6)
        
        const submitData = {
          title: examForm.title,
          description: examForm.description,
          subject_id: examForm.subject_id,
          duration: examForm.duration,
          passing_score: passingScore,
          start_time: examForm.start_time,
          end_time: examForm.end_time,
          status: examForm.status,
          question_ids: selectedQuestions.value.map(q => q.id),
          question_count: selectedQuestions.value.length,
          total_points: totalPoints.value,
          settings: settingsForm
        }
        
        if (isEditMode.value && examId.value) {
          // 更新现有考试
          await examApi.updateExam(examId.value, submitData)
          ElMessage.success('考试更新成功')
        } else {
          // 创建新考试
          await examApi.createExam(submitData)
        ElMessage.success('考试创建成功')
        }
        
        router.push('/admin/exams')
      } catch (error) {
        const action = isEditMode.value ? '更新' : '创建'
        ElMessage.error(`${action}考试失败`)
        console.error('Submit exam error:', error)
      } finally {
        submitting.value = false
      }
    }
    
    const getSubjectName = (subjectId) => {
      const subject = subjects.value.find(s => s.id === subjectId)
      return subject ? subject.name : ''
    }
    
    const getTypeLabel = (type) => {
      const labels = {
        'single': '单选题',
        'multiple': '多选题',
        'judge': '判断题',
        'fill': '填空题',
        'essay': '简答题'
      }
      return labels[type] || type
    }
    
    const getDifficultyLabel = (difficulty) => {
      const labels = {
        'easy': '简单',
        'medium': '中等',
        'hard': '困难'
      }
      return labels[difficulty] || difficulty
    }
    
    const formatDate = (date) => {
      if (!date) return ''
      const d = new Date(date)
      if (isNaN(d.getTime())) return ''
      return d.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const loadExistingExam = async () => {
      if (!isEditMode.value || !examId.value) return
      
      try {
        const response = await examApi.getExam(examId.value)
        const exam = response.data
        
        // 填充基本信息
        Object.assign(examForm, {
          title: exam.title,
          description: exam.description || '',
          subject_id: exam.subject_id,
          duration: exam.duration,
          passing_score: exam.passing_score || null,
          start_time: exam.start_time ? new Date(exam.start_time) : null,
          end_time: exam.end_time ? new Date(exam.end_time) : null,
          status: exam.status
        })
        
        // 填充考试设置
        if (exam.settings) {
          Object.assign(settingsForm, {
            shuffle_questions: exam.settings.shuffle_questions || false,
            shuffle_options: exam.settings.shuffle_options || false,
            show_answer: exam.settings.show_answer || false,
            show_explanation: exam.settings.show_explanation || false,
            allow_retake: exam.settings.allow_retake || false
          })
        }
        
        // 加载已选择的试题
        if (exam.question_ids && exam.question_ids.length > 0) {
          const questionIds = exam.question_ids.join(',')
          const questionsResponse = await questionApi.getQuestions({ ids: questionIds })
          selectedQuestions.value = questionsResponse.data.items || questionsResponse.data || []
        }
        
        ElMessage.success('考试数据加载成功')
      } catch (error) {
        ElMessage.error('加载考试数据失败')
        console.error('Load existing exam error:', error)
        router.push('/admin/exams')
      }
    }
    
    onMounted(async () => {
      await loadSubjects()
      if (isEditMode.value) {
        await loadExistingExam()
      }
    })
    
    return {
      currentStep,
      submitting,
      isEditMode,
      examId,
      subjects,
      availableQuestions,
      selectedQuestions,
      questionSelectMode,
      questionSearch,
      questionType,
      questionDifficulty,
      basicFormRef,
      loadingQuestions,
      examForm,
      randomForm,
      settingsForm,
      basicRules,
      totalPoints,
      handleSubjectChange,
      searchQuestions,
      handleQuestionSelect,
      removeQuestion,
      generateRandomQuestions,
      nextStep,
      prevStep,
      submitExam,
      getSubjectName,
      getTypeLabel,
      getDifficultyLabel,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-exam-creation {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0 0 32px 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.modern-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 24px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .header-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
    
    .header-left {
      .page-title {
        display: flex;
        align-items: center;
        gap: 20px;
        
        .title-icon {
          width: 64px;
          height: 64px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.3);
          
          .el-icon {
            font-size: 32px;
            color: white;
          }
        }
        
        .title-text {
          h1 {
            font-size: 32px;
            font-weight: 700;
            color: white;
            margin: 0 0 8px 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          }
          
          p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            margin: 0;
            font-weight: 500;
          }
        }
      }
    }
    
    .header-right {
      .back-btn {
        padding: 12px 20px;
        font-weight: 600;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
        color: white;
        
        &:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-2px);
        }
      }
    }
  }
}

.steps-section {
  padding: 32px;
  
  .steps-container {
    max-width: 1400px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  }
}

.form-section {
  padding: 0 32px;
  
  .form-card {
    max-width: 1400px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    
    .step-content {
      min-height: 400px;
      
      .step-title {
        font-size: 24px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0 0 24px 0;
        padding-bottom: 16px;
        border-bottom: 2px solid #e9ecef;
      }
      
      .question-tabs {
        margin-bottom: 24px;
      }
      
      .manual-selection {
        .search-bar {
          display: flex;
          margin-bottom: 16px;
        }
        
        .question-list {
          margin-top: 16px;
        }
      }
      
      .random-selection {
        max-width: 600px;
      }
      
      .selected-questions {
        margin-top: 24px;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 12px;
        
        h4 {
          font-size: 16px;
          font-weight: 600;
          color: #1a1a1a;
          margin: 0 0 16px 0;
        }
        
        .selected-list {
          max-height: 200px;
          overflow-y: auto;
        }
      }
      
      .preview-content {
        .question-preview {
          h4 {
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
            margin: 0 0 16px 0;
          }
        }
      }
    }
    
    .form-actions {
      margin-top: 32px;
      padding-top: 24px;
      border-top: 2px solid #e9ecef;
      display: flex;
      justify-content: center;
      gap: 16px;
      
      .el-button {
        min-width: 120px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
      }
    }
  }
}

@media (max-width: 768px) {
  .modern-header .header-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
    padding: 0 16px;
  }
  
  .steps-section {
    padding: 16px;
    
    .steps-container {
      padding: 20px;
    }
  }
  
  .form-section {
    padding: 0 16px;
    
    .form-card {
      padding: 20px;
      
      .step-content {
        .manual-selection .search-bar {
          flex-direction: column;
          gap: 12px;
          
          .el-select {
            width: 100% !important;
            margin-left: 0 !important;
          }
          
          .el-button {
            width: 100%;
            margin-left: 0 !important;
          }
        }
      }
    }
  }
}
</style>
