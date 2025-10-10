<template>
  <div class="question-import">
    <el-steps :active="currentStep" finish-status="success">
      <el-step title="选择文件" />
      <el-step title="预览数据" />
      <el-step title="导入完成" />
    </el-steps>

    <!-- 步骤1：选择文件 -->
    <div v-if="currentStep === 0" class="step-content">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>选择导入文件</span>
            <el-button type="text" @click="downloadTemplate">
              <el-icon><Download /></el-icon>
              下载模板
            </el-button>
          </div>
        </template>

        <el-form :model="importForm" label-width="100px">
          <el-form-item label="选择科目" required>
            <el-select
              v-model="importForm.subject_id"
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

          <el-form-item label="上传文件" required>
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :on-change="handleFileChange"
              :before-upload="beforeUpload"
              accept=".xlsx,.xls"
              :limit="1"
              drag
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  只能上传 xlsx/xls 文件，且不超过 10MB
                </div>
              </template>
            </el-upload>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              @click="nextStep"
              :disabled="!importForm.subject_id || !importForm.file"
            >
              下一步
            </el-button>
            <el-button @click="handleCancel">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 步骤2：预览数据 -->
    <div v-if="currentStep === 1" class="step-content">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>预览导入数据</span>
            <el-tag type="info">共 {{ previewData.length }} 条数据</el-tag>
          </div>
        </template>

        <div class="preview-table">
          <el-table
            :data="previewData.slice(0, 10)"
            border
            stripe
            max-height="400"
          >
            <el-table-column prop="title" label="题目标题" min-width="200" show-overflow-tooltip />
            <el-table-column prop="type" label="题型" width="100">
              <template #default="{ row }">
                <el-tag :type="getTypeTagType(row.type)" size="small">
                  {{ getTypeLabel(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="80">
              <template #default="{ row }">
                <el-tag :type="getDifficultyTagType(row.difficulty)" size="small">
                  {{ getDifficultyLabel(row.difficulty) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="points" label="分值" width="60" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row.status)" size="small">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="validation" label="验证结果" width="100">
              <template #default="{ row }">
                <el-tag
                  :type="row.validation.valid ? 'success' : 'danger'"
                  size="small"
                >
                  {{ row.validation.valid ? '有效' : '无效' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="validation.message" label="错误信息" min-width="150" show-overflow-tooltip />
          </el-table>

          <div v-if="previewData.length > 10" class="preview-tip">
            <el-alert
              title="仅显示前10条数据，实际导入时会处理所有数据"
              type="info"
              :closable="false"
            />
          </div>
        </div>

        <div class="preview-summary">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-statistic title="总数据" :value="previewData.length" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="有效数据" :value="validCount" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="无效数据" :value="invalidCount" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="成功率" :value="successRate" suffix="%" />
            </el-col>
          </el-row>
        </div>

        <div class="step-actions">
          <el-button @click="prevStep">上一步</el-button>
          <el-button
            type="primary"
            @click="startImport"
            :loading="importing"
            :disabled="validCount === 0"
          >
            开始导入
          </el-button>
          <el-button @click="handleCancel">取消</el-button>
        </div>
      </el-card>
    </div>

    <!-- 步骤3：导入完成 -->
    <div v-if="currentStep === 2" class="step-content">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>导入完成</span>
            <el-tag :type="importResult.success_count > 0 ? 'success' : 'danger'">
              {{ importResult.success_count > 0 ? '成功' : '失败' }}
            </el-tag>
          </div>
        </template>

        <div class="import-result">
          <el-result
            :icon="importResult.success_count > 0 ? 'success' : 'error'"
            :title="importResult.success_count > 0 ? '导入成功' : '导入失败'"
            :sub-title="getResultMessage()"
          >
            <template #extra>
              <div class="result-stats">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-statistic title="成功导入" :value="importResult.success_count" />
                  </el-col>
                  <el-col :span="8">
                    <el-statistic title="导入失败" :value="importResult.error_count" />
                  </el-col>
                  <el-col :span="8">
                    <el-statistic title="成功率" :value="successRate" suffix="%" />
                  </el-col>
                </el-row>
              </div>

              <div v-if="importResult.errors && importResult.errors.length > 0" class="error-details">
                <el-collapse>
                  <el-collapse-item title="错误详情" name="errors">
                    <div class="error-list">
                      <div
                        v-for="(error, index) in importResult.errors"
                        :key="index"
                        class="error-item"
                      >
                        <el-tag type="danger" size="small">第{{ error.row }}行</el-tag>
                        <span>{{ error.message }}</span>
                      </div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </div>

              <div class="result-actions">
                <el-button type="primary" @click="handleSuccess">完成</el-button>
                <el-button @click="resetImport">重新导入</el-button>
              </div>
            </template>
          </el-result>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Download } from '@element-plus/icons-vue'
import { questionApi } from '@/api/questions'
import * as XLSX from 'xlsx'

export default {
  name: 'QuestionImport',
  components: {
    UploadFilled,
    Download
  },
  props: {
    subjects: {
      type: Array,
      default: () => []
    }
  },
  emits: ['success', 'cancel'],
  setup(props, { emit }) {
    const uploadRef = ref()
    const currentStep = ref(0)
    const importing = ref(false)
    const previewData = ref([])
    const importResult = ref({})

    // 导入表单
    const importForm = reactive({
      subject_id: '',
      file: null
    })

    // 计算属性
    const validCount = computed(() => {
      return previewData.value.filter(item => item.validation.valid).length
    })

    const invalidCount = computed(() => {
      return previewData.value.filter(item => !item.validation.valid).length
    })

    const successRate = computed(() => {
      if (previewData.value.length === 0) return 0
      return Math.round((validCount.value / previewData.value.length) * 100)
    })

    // 方法
    const downloadTemplate = async () => {
      try {
        await questionApi.getImportTemplate()
        ElMessage.success('模板下载成功')
      } catch (error) {
        ElMessage.error('下载模板失败')
        console.error('Download template error:', error)
      }
    }

    const handleFileChange = (file) => {
      importForm.file = file.raw
    }

    const beforeUpload = (file) => {
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                     file.type === 'application/vnd.ms-excel'
      if (!isExcel) {
        ElMessage.error('只能上传 Excel 文件!')
        return false
      }
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        ElMessage.error('文件大小不能超过 10MB!')
        return false
      }
      return false // 阻止自动上传
    }

    const nextStep = async () => {
      if (!importForm.subject_id || !importForm.file) {
        ElMessage.error('请选择科目和上传文件')
        return
      }

      try {
        // 解析Excel文件
        const workbook = XLSX.read(importForm.file, { type: 'array' })
        const sheetName = workbook.SheetNames[0]
        const worksheet = workbook.Sheets[sheetName]
        const data = XLSX.utils.sheet_to_json(worksheet)

        // 验证和转换数据
        previewData.value = data.map((row, index) => {
          const validation = validateQuestionData(row, index + 2) // +2 因为Excel从第2行开始
          return {
            ...row,
            validation
          }
        })

        currentStep.value = 1
      } catch (error) {
        ElMessage.error('文件解析失败')
        console.error('Parse file error:', error)
      }
    }

    const validateQuestionData = (data, row) => {
      const errors = []

      // 验证必填字段
      if (!data.title || data.title.trim() === '') {
        errors.push('题目标题不能为空')
      }

      if (!data.type || !['single', 'multiple', 'judge', 'fill', 'essay'].includes(data.type)) {
        errors.push('题型必须是：single, multiple, judge, fill, essay')
      }

      if (!data.difficulty || !['easy', 'medium', 'hard'].includes(data.difficulty)) {
        errors.push('难度必须是：easy, medium, hard')
      }

      if (!data.answer || data.answer.trim() === '') {
        errors.push('答案不能为空')
      }

      // 验证选项
      if (['single', 'multiple'].includes(data.type)) {
        if (!data.options || data.options.trim() === '') {
          errors.push('选择题必须提供选项')
        } else {
          try {
            const options = JSON.parse(data.options)
            if (!Array.isArray(options) || options.length < 2) {
              errors.push('选项必须是至少包含2个选项的数组')
            }
          } catch (e) {
            errors.push('选项格式错误，必须是JSON数组格式')
          }
        }
      }

      return {
        valid: errors.length === 0,
        message: errors.join('; ')
      }
    }

    const prevStep = () => {
      currentStep.value = 0
    }

    const startImport = async () => {
      try {
        importing.value = true
        
        // 准备导入数据
        const validData = previewData.value
          .filter(item => item.validation.valid)
          .map(item => ({
            subject_id: importForm.subject_id,
            type: item.type,
            title: item.title,
            content: item.content || '',
            options: item.options ? JSON.parse(item.options) : [],
            answer: item.answer,
            explanation: item.explanation || '',
            difficulty: item.difficulty,
            points: parseInt(item.points) || 1,
            status: item.status || 'draft',
            tags: item.tags ? item.tags.split(',').map(tag => tag.trim()) : []
          }))

        // 调用导入API
        const result = await questionApi.importQuestions({
          subject_id: importForm.subject_id,
          questions: validData
        })

        importResult.value = result.data
        currentStep.value = 2
      } catch (error) {
        ElMessage.error('导入失败')
        console.error('Import error:', error)
      } finally {
        importing.value = false
      }
    }

    const getResultMessage = () => {
      const { success_count, error_count } = importResult.value
      if (success_count > 0 && error_count === 0) {
        return `成功导入 ${success_count} 个试题`
      } else if (success_count > 0 && error_count > 0) {
        return `成功导入 ${success_count} 个试题，${error_count} 个失败`
      } else {
        return '导入失败，请检查数据格式'
      }
    }

    const handleSuccess = () => {
      emit('success')
    }

    const resetImport = () => {
      currentStep.value = 0
      importForm.subject_id = ''
      importForm.file = null
      previewData.value = []
      importResult.value = {}
      uploadRef.value?.clearFiles()
    }

    const handleCancel = () => {
      emit('cancel')
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

    const getStatusLabel = (status) => {
      const labels = {
        draft: '草稿',
        published: '已发布',
        archived: '已归档'
      }
      return labels[status] || status
    }

    const getStatusTagType = (status) => {
      const types = {
        draft: 'info',
        published: 'success',
        archived: 'warning'
      }
      return types[status] || 'default'
    }

    return {
      uploadRef,
      currentStep,
      importing,
      previewData,
      importResult,
      importForm,
      validCount,
      invalidCount,
      successRate,
      downloadTemplate,
      handleFileChange,
      beforeUpload,
      nextStep,
      prevStep,
      startImport,
      getResultMessage,
      handleSuccess,
      resetImport,
      handleCancel,
      getTypeLabel,
      getTypeTagType,
      getDifficultyLabel,
      getDifficultyTagType,
      getStatusLabel,
      getStatusTagType
    }
  }
}
</script>

<style scoped>
.question-import {
  padding: 20px;
}

.step-content {
  margin-top: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-table {
  margin-bottom: 20px;
}

.preview-tip {
  margin-top: 15px;
}

.preview-summary {
  margin: 20px 0;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.step-actions {
  margin-top: 30px;
  text-align: center;
}

.import-result {
  padding: 20px;
}

.result-stats {
  margin: 20px 0;
}

.error-details {
  margin: 20px 0;
}

.error-list {
  max-height: 200px;
  overflow-y: auto;
}

.error-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 10px;
}

.result-actions {
  margin-top: 30px;
  text-align: center;
}

:deep(.el-upload-dragger) {
  width: 100%;
}

:deep(.el-steps) {
  margin-bottom: 30px;
}
</style>
