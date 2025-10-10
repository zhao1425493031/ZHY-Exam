<template>
  <div class="exam-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      @submit.prevent="handleSubmit"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="考试标题" prop="title">
            <el-input
              v-model="form.title"
              placeholder="请输入考试标题"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="科目" prop="subject_id">
            <el-select
              v-model="form.subject_id"
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
        </el-col>
      </el-row>

      <el-form-item label="考试描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入考试描述"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="考试时长" prop="duration">
            <el-input-number
              v-model="form.duration"
              :min="1"
              :max="480"
              style="width: 100%"
            />
            <span class="form-tip">分钟</span>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="状态" prop="status">
            <el-select
              v-model="form.status"
              placeholder="请选择状态"
              style="width: 100%"
            >
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="组卷方式" prop="paper_type">
            <el-select
              v-model="form.paper_type"
              placeholder="请选择组卷方式"
              style="width: 100%"
              @change="handlePaperTypeChange"
            >
              <el-option label="随机组卷" value="random" />
              <el-option label="手动选题" value="manual" />
              <el-option label="模板组卷" value="template" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">时间设置</el-divider>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="开始时间">
            <el-date-picker
              v-model="form.start_time"
              type="datetime"
              placeholder="选择开始时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DD HH:mm:ss"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="结束时间">
            <el-date-picker
              v-model="form.end_time"
              type="datetime"
              placeholder="选择结束时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DD HH:mm:ss"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 随机组卷配置 -->
      <div v-if="form.paper_type === 'random'">
        <el-divider content-position="left">随机组卷配置</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="题目总数" prop="total_questions">
              <el-input-number
                v-model="form.total_questions"
                :min="1"
                :max="100"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="题型选择">
              <el-checkbox-group v-model="form.question_types">
                <el-checkbox label="single">单选题</el-checkbox>
                <el-checkbox label="multiple">多选题</el-checkbox>
                <el-checkbox label="judge">判断题</el-checkbox>
                <el-checkbox label="fill">填空题</el-checkbox>
                <el-checkbox label="essay">简答题</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="难度分布">
              <div class="difficulty-distribution">
                <div class="difficulty-item">
                  <span class="difficulty-label">简单：</span>
                  <el-input-number
                    v-model="form.difficulty_distribution.easy"
                    :min="0"
                    :max="100"
                    :precision="1"
                    size="small"
                  />
                  <span class="difficulty-unit">%</span>
                </div>
                <div class="difficulty-item">
                  <span class="difficulty-label">中等：</span>
                  <el-input-number
                    v-model="form.difficulty_distribution.medium"
                    :min="0"
                    :max="100"
                    :precision="1"
                    size="small"
                  />
                  <span class="difficulty-unit">%</span>
                </div>
                <div class="difficulty-item">
                  <span class="difficulty-label">困难：</span>
                  <el-input-number
                    v-model="form.difficulty_distribution.hard"
                    :min="0"
                    :max="100"
                    :precision="1"
                    size="small"
                  />
                  <span class="difficulty-unit">%</span>
                </div>
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="预览配置">
              <div class="config-preview">
                <div class="preview-item">
                  <span class="preview-label">预计题目数：</span>
                  <span class="preview-value">{{ form.total_questions || 0 }}题</span>
                </div>
                <div class="preview-item">
                  <span class="preview-label">预计时长：</span>
                  <span class="preview-value">{{ calculatedDuration }}分钟</span>
                </div>
                <div class="preview-item">
                  <span class="preview-label">难度分布：</span>
                  <span class="preview-value">
                    简单{{ form.difficulty_distribution.easy }}% | 
                    中等{{ form.difficulty_distribution.medium }}% | 
                    困难{{ form.difficulty_distribution.hard }}%
                  </span>
                </div>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 手动选题配置 -->
      <div v-if="form.paper_type === 'manual'">
        <el-divider content-position="left">手动选题</el-divider>
        
        <el-form-item label="选择题目">
          <div class="question-selector">
            <div class="selector-header">
              <el-button type="primary" @click="showQuestionSelector = true">
                选择题目
              </el-button>
              <span class="selected-count">已选择 {{ selectedQuestions.length }} 题</span>
            </div>
            
            <div v-if="selectedQuestions.length > 0" class="selected-questions">
              <div
                v-for="question in selectedQuestions"
                :key="question.id"
                class="question-item"
              >
                <div class="question-info">
                  <span class="question-title">{{ question.title }}</span>
                  <div class="question-meta">
                    <el-tag :type="getTypeTagType(question.type)" size="small">
                      {{ getTypeLabel(question.type) }}
                    </el-tag>
                    <el-tag :type="getDifficultyTagType(question.difficulty)" size="small">
                      {{ getDifficultyLabel(question.difficulty) }}
                    </el-tag>
                    <span class="question-points">{{ question.points }}分</span>
                  </div>
                </div>
                <el-button
                  type="danger"
                  size="small"
                  @click="removeQuestion(question.id)"
                >
                  移除
                </el-button>
              </div>
            </div>
          </div>
        </el-form-item>
      </div>

      <!-- 模板组卷配置 -->
      <div v-if="form.paper_type === 'template'">
        <el-divider content-position="left">模板组卷</el-divider>
        
        <el-form-item label="选择模板">
          <el-select
            v-model="form.template_id"
            placeholder="请选择考试模板"
            style="width: 100%"
          >
            <el-option
              v-for="template in examTemplates"
              :key="template.id"
              :label="template.name"
              :value="template.id"
            />
          </el-select>
        </el-form-item>
      </div>

      <el-divider content-position="left">考试设置</el-divider>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="允许重考">
            <el-switch v-model="form.settings.allow_retake" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="显示答案">
            <el-switch v-model="form.settings.show_answer" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="防切屏">
            <el-switch v-model="form.settings.prevent_switch" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="自动提交">
            <el-switch v-model="form.settings.auto_submit" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ exam ? '更新' : '创建' }}
        </el-button>
        <el-button @click="handleCancel">取消</el-button>
        <el-button v-if="exam" @click="handlePreview">预览</el-button>
      </el-form-item>
    </el-form>

    <!-- 题目选择器对话框 -->
    <el-dialog
      v-model="showQuestionSelector"
      title="选择题目"
      width="80%"
    >
      <QuestionSelector
        v-if="showQuestionSelector"
        :subject-id="form.subject_id"
        :selected-questions="selectedQuestions"
        @confirm="handleQuestionSelect"
        @cancel="showQuestionSelector = false"
      />
    </el-dialog>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="showPreview"
      title="考试预览"
      width="60%"
    >
      <ExamPreview
        v-if="showPreview"
        :exam="form"
        :subjects="subjects"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import QuestionSelector from '@/components/exam/QuestionSelector.vue'
import ExamPreview from '@/components/exam/ExamPreview.vue'
import { examApi } from '@/api/exams'

export default {
  name: 'ExamForm',
  components: {
    QuestionSelector,
    ExamPreview
  },
  props: {
    exam: {
      type: Object,
      default: null
    },
    subjects: {
      type: Array,
      default: () => []
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const formRef = ref()
    const submitting = ref(false)
    const showQuestionSelector = ref(false)
    const showPreview = ref(false)
    const selectedQuestions = ref([])
    const examTemplates = ref([])

    // 表单数据
    const form = reactive({
      title: '',
      subject_id: '',
      description: '',
      duration: 60,
      status: 'draft',
      paper_type: 'random',
      start_time: '',
      end_time: '',
      total_questions: 10,
      question_types: ['single', 'multiple', 'judge'],
      difficulty_distribution: {
        easy: 30,
        medium: 50,
        hard: 20
      },
      template_id: '',
      settings: {
        allow_retake: false,
        show_answer: true,
        prevent_switch: false,
        auto_submit: true
      }
    })

    // 表单验证规则
    const rules = {
      title: [
        { required: true, message: '请输入考试标题', trigger: 'blur' },
        { min: 2, message: '考试标题至少2个字符', trigger: 'blur' },
        { max: 200, message: '考试标题不能超过200个字符', trigger: 'blur' }
      ],
      subject_id: [
        { required: true, message: '请选择科目', trigger: 'change' }
      ],
      duration: [
        { required: true, message: '请输入考试时长', trigger: 'blur' },
        { type: 'number', min: 1, max: 480, message: '考试时长必须在1-480分钟之间', trigger: 'blur' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ],
      paper_type: [
        { required: true, message: '请选择组卷方式', trigger: 'change' }
      ],
      total_questions: [
        { required: true, message: '请输入题目总数', trigger: 'blur' },
        { type: 'number', min: 1, max: 100, message: '题目总数必须在1-100之间', trigger: 'blur' }
      ]
    }

    // 计算属性
    const calculatedDuration = computed(() => {
      if (form.paper_type === 'manual') {
        return selectedQuestions.value.reduce((total, q) => {
          const timePerQuestion = {
            single: 2,
            multiple: 3,
            judge: 1,
            fill: 5,
            essay: 10
          }
          return total + (timePerQuestion[q.type] || 3)
        }, 0)
      } else if (form.paper_type === 'random') {
        const timePerQuestion = {
          single: 2,
          multiple: 3,
          judge: 1,
          fill: 5,
          essay: 10
        }
        return form.question_types.reduce((total, type) => {
          const count = Math.ceil(form.total_questions * (form.difficulty_distribution[type] || 0) / 100)
          return total + (count * (timePerQuestion[type] || 3))
        }, 0)
      }
      return form.duration
    })

    // 方法
    const handleSubjectChange = () => {
      // 清空相关配置
      selectedQuestions.value = []
      form.template_id = ''
    }

    const handlePaperTypeChange = () => {
      // 重置相关配置
      selectedQuestions.value = []
      form.template_id = ''
    }

    const handleQuestionSelect = (questions) => {
      selectedQuestions.value = questions
      showQuestionSelector.value = false
      
      // 更新表单数据
      form.question_ids = questions.map(q => q.id)
      form.question_count = questions.length
      form.total_points = questions.reduce((total, q) => total + q.points, 0)
    }

    const removeQuestion = (questionId) => {
      const index = selectedQuestions.value.findIndex(q => q.id === questionId)
      if (index > -1) {
        selectedQuestions.value.splice(index, 1)
        
        // 更新表单数据
        form.question_ids = selectedQuestions.value.map(q => q.id)
        form.question_count = selectedQuestions.value.length
        form.total_points = selectedQuestions.value.reduce((total, q) => total + q.points, 0)
      }
    }

    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        
        // 验证难度分布
        if (form.paper_type === 'random') {
          const totalRatio = form.difficulty_distribution.easy + 
                           form.difficulty_distribution.medium + 
                           form.difficulty_distribution.hard
          if (Math.abs(totalRatio - 100) > 0.1) {
            ElMessage.error('难度分布比例之和必须等于100%')
            return
          }
        }

        // 验证手动选题
        if (form.paper_type === 'manual' && selectedQuestions.value.length === 0) {
          ElMessage.error('请至少选择一道题目')
          return
        }

        // 验证模板组卷
        if (form.paper_type === 'template' && !form.template_id) {
          ElMessage.error('请选择考试模板')
          return
        }

        // 准备提交数据
        const submitData = { ...form }
        
        if (form.paper_type === 'manual') {
          submitData.question_ids = selectedQuestions.value.map(q => q.id)
          submitData.question_count = selectedQuestions.value.length
          submitData.total_points = selectedQuestions.value.reduce((total, q) => total + q.points, 0)
        }

        submitting.value = true
        emit('submit', submitData)
      } catch (error) {
        console.error('Form validation error:', error)
      } finally {
        submitting.value = false
      }
    }

    const handleCancel = () => {
      emit('cancel')
    }

    const handlePreview = () => {
      showPreview.value = true
    }

    // 工具方法
    const getTypeLabel = (type) => {
      const labels = {
        single: '单选题',
        multiple: '多选题',
        judge: '判断题',
        fill: '填空题',
        essay: '简答题'
      }
      return labels[type] || type
    }

    const getTypeTagType = (type) => {
      const types = {
        single: 'primary',
        multiple: 'success',
        judge: 'warning',
        fill: 'info',
        essay: 'danger'
      }
      return types[type] || 'default'
    }

    const getDifficultyLabel = (difficulty) => {
      const labels = {
        easy: '简单',
        medium: '中等',
        hard: '困难'
      }
      return labels[difficulty] || difficulty
    }

    const getDifficultyTagType = (difficulty) => {
      const types = {
        easy: 'success',
        medium: 'warning',
        hard: 'danger'
      }
      return types[difficulty] || 'default'
    }

    // 监听难度分布变化
    watch(() => form.difficulty_distribution, (newVal) => {
      const total = newVal.easy + newVal.medium + newVal.hard
      if (total > 100) {
        ElMessage.warning('难度分布比例之和不能超过100%')
      }
    }, { deep: true })

    // 初始化表单数据
    const initForm = () => {
      if (props.exam) {
        Object.assign(form, props.exam)
        
        // 处理题目数据
        if (props.exam.question_ids && Array.isArray(props.exam.question_ids)) {
          // TODO: 加载题目详情
          selectedQuestions.value = []
        }
      }
    }

    // 加载考试模板
    const loadExamTemplates = async () => {
      try {
        // TODO: 实现加载考试模板API
        examTemplates.value = []
      } catch (error) {
        console.error('Load exam templates error:', error)
      }
    }

    // 组件挂载时初始化
    onMounted(() => {
      initForm()
      loadExamTemplates()
    })

    return {
      formRef,
      submitting,
      showQuestionSelector,
      showPreview,
      selectedQuestions,
      examTemplates,
      form,
      rules,
      calculatedDuration,
      handleSubjectChange,
      handlePaperTypeChange,
      handleQuestionSelect,
      removeQuestion,
      handleSubmit,
      handleCancel,
      handlePreview,
      getTypeLabel,
      getTypeTagType,
      getDifficultyLabel,
      getDifficultyTagType
    }
  }
}
</script>

<style scoped>
.exam-form {
  padding: 20px;
}

.form-tip {
  margin-left: 5px;
  color: #909399;
  font-size: 14px;
}

.difficulty-distribution {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.difficulty-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.difficulty-label {
  min-width: 50px;
  color: #606266;
  font-size: 14px;
}

.difficulty-unit {
  color: #909399;
  font-size: 12px;
}

.config-preview {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.preview-item {
  margin-bottom: 8px;
}

.preview-item:last-child {
  margin-bottom: 0;
}

.preview-label {
  color: #606266;
  font-weight: 500;
}

.preview-value {
  color: #303133;
}

.question-selector {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
}

.selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.selected-count {
  color: #606266;
  font-size: 14px;
}

.selected-questions {
  max-height: 300px;
  overflow-y: auto;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.question-item:last-child {
  margin-bottom: 0;
}

.question-info {
  flex: 1;
}

.question-title {
  display: block;
  margin-bottom: 8px;
  color: #303133;
  font-weight: 500;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.question-points {
  color: #e6a23c;
  font-weight: 500;
  font-size: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-textarea__inner) {
  resize: vertical;
}

:deep(.el-divider__text) {
  font-weight: 500;
  color: #303133;
}
</style>
