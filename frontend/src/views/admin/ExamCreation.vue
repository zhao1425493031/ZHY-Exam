<template>
  <div class="exam-creation">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>考试创建</span>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="考试标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入考试标题" />
        </el-form-item>
        
        <el-form-item label="考试描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入考试描述"
          />
        </el-form-item>
        
        <el-form-item label="科目" prop="subject_id">
          <el-select v-model="form.subject_id" placeholder="请选择科目">
            <el-option
              v-for="subject in subjects"
              :key="subject.id"
              :label="subject.name"
              :value="subject.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="考试时长" prop="duration">
          <el-input-number
            v-model="form.duration"
            :min="1"
            :max="300"
            placeholder="分钟"
          />
          <span style="margin-left: 10px;">分钟</span>
        </el-form-item>
        
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择开始时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选择结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        
        <el-form-item label="组卷方式" prop="question_selection_type">
          <el-radio-group v-model="form.question_selection_type">
            <el-radio value="manual">手动选题</el-radio>
            <el-radio value="random">随机组卷</el-radio>
            <el-radio value="template">使用模板</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 手动选题 -->
        <div v-if="form.question_selection_type === 'manual'">
          <el-form-item label="选择题目">
            <el-button type="primary" @click="showQuestionSelector = true">选择题目</el-button>
            <span style="margin-left: 10px;">已选择 {{ selectedQuestions.length }} 道题目</span>
          </el-form-item>
        </div>
        
        <!-- 随机组卷 -->
        <div v-if="form.question_selection_type === 'random'">
          <el-form-item label="题目数量" prop="question_count">
            <el-input-number
              v-model="form.question_count"
              :min="1"
              :max="100"
              placeholder="题目数量"
            />
          </el-form-item>
          
          <el-form-item label="难度分布">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="简单">
                  <el-input-number
                    v-model="form.difficulty_distribution.easy"
                    :min="0"
                    :max="form.question_count"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="中等">
                  <el-input-number
                    v-model="form.difficulty_distribution.medium"
                    :min="0"
                    :max="form.question_count"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="困难">
                  <el-input-number
                    v-model="form.difficulty_distribution.hard"
                    :min="0"
                    :max="form.question_count"
                  />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form-item>
        </div>
        
        <!-- 使用模板 -->
        <div v-if="form.question_selection_type === 'template'">
          <el-form-item label="选择模板" prop="template_id">
            <el-select v-model="form.template_id" placeholder="请选择模板">
              <el-option
                v-for="template in templates"
                :key="template.id"
                :label="template.name"
                :value="template.id"
              />
            </el-select>
          </el-form-item>
        </div>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">创建考试</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 题目选择器 -->
    <el-dialog
      v-model="showQuestionSelector"
      title="选择题目"
      width="80%"
      @close="showQuestionSelector = false"
    >
      <QuestionSelector
        :selected-questions="selectedQuestions"
        @update:selected-questions="handleQuestionSelection"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import QuestionSelector from '@/components/exam/QuestionSelector.vue'

export default {
  name: 'ExamCreation',
  components: {
    QuestionSelector
  },
  setup() {
    const formRef = ref()
    const showQuestionSelector = ref(false)
    
    const subjects = ref([])
    const templates = ref([])
    const selectedQuestions = ref([])
    
    const form = reactive({
      title: '',
      description: '',
      subject_id: null,
      duration: 120,
      start_time: '',
      end_time: '',
      question_selection_type: 'manual',
      question_count: 20,
      difficulty_distribution: {
        easy: 5,
        medium: 10,
        hard: 5
      },
      template_id: null
    })
    
    const rules = {
      title: [
        { required: true, message: '请输入考试标题', trigger: 'blur' }
      ],
      subject_id: [
        { required: true, message: '请选择科目', trigger: 'change' }
      ],
      duration: [
        { required: true, message: '请输入考试时长', trigger: 'blur' }
      ],
      question_selection_type: [
        { required: true, message: '请选择组卷方式', trigger: 'change' }
      ]
    }
    
    const loadSubjects = async () => {
      // 模拟数据，实际应该调用API
      subjects.value = [
        { id: 1, name: 'Vue.js' },
        { id: 2, name: 'JavaScript' },
        { id: 3, name: 'Python' }
      ]
    }
    
    const loadTemplates = async () => {
      // 模拟数据，实际应该调用API
      templates.value = [
        { id: 1, name: 'Vue.js基础考试模板' },
        { id: 2, name: 'JavaScript进阶考试模板' }
      ]
    }
    
    const handleQuestionSelection = (questions) => {
      selectedQuestions.value = questions
    }
    
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        
        const examData = {
          ...form,
          question_ids: selectedQuestions.value.map(q => q.id)
        }
        
        // 实际应该调用创建考试API
        console.log('创建考试数据:', examData)
        ElMessage.success('考试创建成功')
        
        // 重置表单
        handleReset()
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }
    
    const handleReset = () => {
      Object.assign(form, {
        title: '',
        description: '',
        subject_id: null,
        duration: 120,
        start_time: '',
        end_time: '',
        question_selection_type: 'manual',
        question_count: 20,
        difficulty_distribution: {
          easy: 5,
          medium: 10,
          hard: 5
        },
        template_id: null
      })
      selectedQuestions.value = []
      formRef.value?.resetFields()
    }
    
    onMounted(() => {
      loadSubjects()
      loadTemplates()
    })
    
    return {
      formRef,
      showQuestionSelector,
      subjects,
      templates,
      selectedQuestions,
      form,
      rules,
      handleQuestionSelection,
      handleSubmit,
      handleReset
    }
  }
}
</script>

<style scoped>
.exam-creation {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>


