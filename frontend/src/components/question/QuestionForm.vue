<template>
  <div class="question-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      @submit.prevent="handleSubmit"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="科目" prop="subject_id">
            <el-select
              v-model="form.subject_id"
              placeholder="请选择科目"
              style="width: 100%"
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
        <el-col :span="12">
          <el-form-item label="题型" prop="type">
            <el-select
              v-model="form.type"
              placeholder="请选择题型"
              style="width: 100%"
              @change="handleTypeChange"
            >
              <el-option label="单选题" value="single" />
              <el-option label="多选题" value="multiple" />
              <el-option label="判断题" value="judge" />
              <el-option label="填空题" value="fill" />
              <el-option label="简答题" value="essay" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="难度" prop="difficulty">
            <el-select
              v-model="form.difficulty"
              placeholder="请选择难度"
              style="width: 100%"
            >
              <el-option label="简单" value="easy" />
              <el-option label="中等" value="medium" />
              <el-option label="困难" value="hard" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="分值" prop="points">
            <el-input-number
              v-model="form.points"
              :min="1"
              :max="100"
              style="width: 100%"
            />
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
              <el-option label="已归档" value="archived" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="题目标题" prop="title">
        <el-input
          v-model="form.title"
          type="textarea"
          :rows="3"
          placeholder="请输入题目标题"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="题目内容" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="4"
          placeholder="请输入题目内容（可选）"
          maxlength="2000"
          show-word-limit
        />
      </el-form-item>

      <!-- 选项部分 -->
      <div v-if="showOptions">
        <el-form-item label="选项设置">
          <div class="options-container">
            <div
              v-for="(option, index) in form.options"
              :key="index"
              class="option-item"
            >
              <el-input
                v-model="option.label"
                placeholder="选项标签（如：A、B、C、D）"
                style="width: 80px; margin-right: 10px"
              />
              <el-input
                v-model="option.text"
                placeholder="选项内容"
                style="flex: 1; margin-right: 10px"
              />
              <el-checkbox
                v-if="form.type === 'multiple'"
                v-model="option.isCorrect"
                style="margin-right: 10px"
              >
                正确
              </el-checkbox>
              <el-radio
                v-else-if="form.type === 'single'"
                v-model="correctOption"
                :label="index"
                style="margin-right: 10px"
              >
                正确
              </el-radio>
              <el-button
                type="danger"
                size="small"
                @click="removeOption(index)"
                :disabled="form.options.length <= 2"
              >
                删除
              </el-button>
            </div>
            <el-button
              type="primary"
              size="small"
              @click="addOption"
              style="margin-top: 10px"
            >
              添加选项
            </el-button>
          </div>
        </el-form-item>
      </div>

      <!-- 判断题选项 -->
      <div v-if="form.type === 'judge'">
        <el-form-item label="正确答案" prop="answer">
          <el-radio-group v-model="form.answer">
            <el-radio label="true">正确</el-radio>
            <el-radio label="false">错误</el-radio>
          </el-radio-group>
        </el-form-item>
      </div>

      <!-- 填空题和简答题答案 -->
      <div v-if="form.type === 'fill' || form.type === 'essay'">
        <el-form-item label="参考答案" prop="answer">
          <el-input
            v-model="form.answer"
            type="textarea"
            :rows="4"
            :placeholder="form.type === 'fill' ? '请输入填空题答案' : '请输入简答题参考答案'"
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
      </div>

      <el-form-item label="解析说明" prop="explanation">
        <el-input
          v-model="form.explanation"
          type="textarea"
          :rows="3"
          placeholder="请输入题目解析说明（可选）"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="标签">
        <el-tag
          v-for="tag in form.tags"
          :key="tag"
          closable
          @close="removeTag(tag)"
          style="margin-right: 10px; margin-bottom: 10px"
        >
          {{ tag }}
        </el-tag>
        <el-input
          v-if="inputVisible"
          ref="inputRef"
          v-model="inputValue"
          class="tag-input"
          size="small"
          @keyup.enter="handleInputConfirm"
          @blur="handleInputConfirm"
        />
        <el-button
          v-else
          class="button-new-tag"
          size="small"
          @click="showInput"
        >
          + 添加标签
        </el-button>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ question ? '更新' : '创建' }}
        </el-button>
        <el-button @click="handleCancel">取消</el-button>
        <el-button v-if="question" @click="handlePreview">预览</el-button>
      </el-form-item>
    </el-form>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="showPreview"
      title="试题预览"
      width="60%"
    >
      <QuestionPreview
        v-if="showPreview"
        :question="form"
        :subjects="subjects"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import QuestionPreview from '@/components/question/QuestionPreview.vue'

export default {
  name: 'QuestionForm',
  components: {
    QuestionPreview
  },
  props: {
    question: {
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
    const inputRef = ref()
    const submitting = ref(false)
    const showPreview = ref(false)
    const inputVisible = ref(false)
    const inputValue = ref('')
    const correctOption = ref(0)

    // 表单数据
    const form = reactive({
      subject_id: '',
      type: 'single',
      title: '',
      content: '',
      options: [
        { label: 'A', text: '', isCorrect: false },
        { label: 'B', text: '', isCorrect: false }
      ],
      answer: '',
      explanation: '',
      difficulty: 'medium',
      points: 1,
      status: 'draft',
      tags: []
    })

    // 表单验证规则
    const rules = {
      subject_id: [
        { required: true, message: '请选择科目', trigger: 'change' }
      ],
      type: [
        { required: true, message: '请选择题型', trigger: 'change' }
      ],
      title: [
        { required: true, message: '请输入题目标题', trigger: 'blur' },
        { min: 5, message: '题目标题至少5个字符', trigger: 'blur' }
      ],
      answer: [
        { required: true, message: '请输入答案', trigger: 'blur' }
      ],
      difficulty: [
        { required: true, message: '请选择难度', trigger: 'change' }
      ],
      points: [
        { required: true, message: '请输入分值', trigger: 'blur' },
        { type: 'number', min: 1, max: 100, message: '分值必须在1-100之间', trigger: 'blur' }
      ]
    }

    // 计算属性
    const showOptions = computed(() => {
      return ['single', 'multiple'].includes(form.type)
    })

    // 监听题型变化
    const handleTypeChange = (type) => {
      // 重置选项
      if (type === 'single' || type === 'multiple') {
        form.options = [
          { label: 'A', text: '', isCorrect: false },
          { label: 'B', text: '', isCorrect: false }
        ]
        correctOption.value = 0
      } else {
        form.options = []
        form.answer = ''
      }
    }

    // 选项操作
    const addOption = () => {
      const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
      const nextLabel = labels[form.options.length]
      form.options.push({
        label: nextLabel,
        text: '',
        isCorrect: false
      })
    }

    const removeOption = (index) => {
      if (form.options.length > 2) {
        form.options.splice(index, 1)
        // 重新设置正确选项
        if (form.type === 'single') {
          if (correctOption.value >= index) {
            correctOption.value = Math.max(0, correctOption.value - 1)
          }
        }
      }
    }

    // 标签操作
    const removeTag = (tag) => {
      const index = form.tags.indexOf(tag)
      if (index > -1) {
        form.tags.splice(index, 1)
      }
    }

    const showInput = () => {
      inputVisible.value = true
      nextTick(() => {
        inputRef.value?.focus()
      })
    }

    const handleInputConfirm = () => {
      if (inputValue.value && !form.tags.includes(inputValue.value)) {
        form.tags.push(inputValue.value)
      }
      inputVisible.value = false
      inputValue.value = ''
    }

    // 表单提交
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        
        // 处理选项答案
        if (form.type === 'single') {
          form.answer = correctOption.value.toString()
        } else if (form.type === 'multiple') {
          const correctOptions = form.options
            .map((option, index) => option.isCorrect ? index : null)
            .filter(index => index !== null)
          form.answer = correctOptions.join(',')
        }

        // 验证选项
        if (showOptions.value) {
          const hasEmptyOption = form.options.some(option => !option.text.trim())
          if (hasEmptyOption) {
            ElMessage.error('请填写所有选项内容')
            return
          }

          const hasCorrectAnswer = form.type === 'single' 
            ? correctOption.value >= 0
            : form.options.some(option => option.isCorrect)
          
          if (!hasCorrectAnswer) {
            ElMessage.error('请设置正确答案')
            return
          }
        }

        submitting.value = true
        emit('submit', { ...form })
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

    // 监听正确选项变化
    watch(correctOption, (newVal) => {
      if (form.type === 'single') {
        form.answer = newVal.toString()
      }
    })

    // 初始化表单数据
    const initForm = () => {
      if (props.question) {
        Object.assign(form, props.question)
        
        // 处理选项
        if (props.question.options && Array.isArray(props.question.options)) {
          form.options = props.question.options.map((option, index) => ({
            label: option.label || String.fromCharCode(65 + index),
            text: option.text || option,
            isCorrect: option.isCorrect || false
          }))
        }

        // 处理单选题答案
        if (form.type === 'single' && form.answer) {
          correctOption.value = parseInt(form.answer) || 0
        }
      }
    }

    // 组件挂载时初始化
    initForm()

    return {
      formRef,
      inputRef,
      submitting,
      showPreview,
      inputVisible,
      inputValue,
      correctOption,
      form,
      rules,
      showOptions,
      handleTypeChange,
      addOption,
      removeOption,
      removeTag,
      showInput,
      handleInputConfirm,
      handleSubmit,
      handleCancel,
      handlePreview
    }
  }
}
</script>

<style scoped>
.question-form {
  padding: 20px;
}

.options-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
  background-color: #fafafa;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.option-item:last-child {
  margin-bottom: 0;
}

.tag-input {
  width: 90px;
  margin-right: 10px;
  vertical-align: bottom;
}

.button-new-tag {
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-textarea__inner) {
  resize: vertical;
}
</style>
