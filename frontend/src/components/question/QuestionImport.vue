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
              show-file-list
              :file-list="fileList"
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
            
            <!-- 上传进度 -->
            <div v-if="uploading" class="upload-progress">
              <el-progress :percentage="uploadProgress" :status="uploadStatus" />
              <p class="upload-text">{{ uploadText }}</p>
            </div>
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
            max-height="500"
            size="small"
          >
            <el-table-column prop="题目" label="题目标题" min-width="200" show-overflow-tooltip />
            <el-table-column prop="内容" label="题目内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="题型" label="题型" width="100">
              <template #default="{ row }">
                <el-tag :type="getTypeTagType(row.题型)" size="small">
                  {{ getTypeLabel(row.题型) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="选项" label="选项" min-width="150" show-overflow-tooltip>
              <template #default="{ row }">
                <div v-if="['single', 'multiple'].includes(row.题型)" class="options-display">
                  {{ formatOptions(row.选项) }}
                </div>
                <span v-else class="no-options">-</span>
              </template>
            </el-table-column>
            <el-table-column prop="答案" label="正确答案" width="100" show-overflow-tooltip>
              <template #default="{ row }">
                <el-tag type="success" size="small">
                  {{ row.答案 }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="解析" label="解析" min-width="150" show-overflow-tooltip />
            <el-table-column prop="标签" label="标签" width="120" show-overflow-tooltip />
            <el-table-column prop="难度" label="难度" width="80">
              <template #default="{ row }">
                <el-tag :type="getDifficultyTagType(row.难度)" size="small">
                  {{ getDifficultyLabel(row.难度) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="分值" label="分值" width="60">
              <template #default="{ row }">
                <el-tag type="info" size="small">
                  {{ row.分值 || 1 }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="状态" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row.状态)" size="small">
                  {{ getStatusLabel(row.状态) }}
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
            <el-table-column prop="validation.message" label="错误信息" min-width="200" show-overflow-tooltip />
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
import { debugExcelParsing, testExcelParsing } from '@/utils/debug-import'

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
    const uploading = ref(false)
    const uploadProgress = ref(0)
    const uploadStatus = ref('')
    const uploadText = ref('')
    const previewData = ref([])
    const importResult = ref({})
    const fileList = ref([])

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
        console.log('开始下载模板...')
        const response = await questionApi.getImportTemplate()
        const blob = new Blob([response], { 
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `Python科目试题导入模板_${new Date().toISOString().slice(0, 10)}.xlsx`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        ElMessage.success('模板下载成功')
      } catch (error) {
        ElMessage.error('下载模板失败')
        console.error('Download template error:', error)
      }
    }

    const handleFileChange = (file, fileListParam) => {
      importForm.file = file.raw
      fileList.value = fileListParam
      
      // 模拟文件上传进度
      uploading.value = true
      uploadProgress.value = 0
      uploadStatus.value = ''
      uploadText.value = '正在读取文件...'
      
      // 模拟上传进度
      const timer = setInterval(() => {
        if (uploadProgress.value < 90) {
          uploadProgress.value += 10
          uploadText.value = `正在解析文件... ${uploadProgress.value}%`
        }
      }, 100)
      
      // 文件读取完成
      setTimeout(() => {
        clearInterval(timer)
        uploadProgress.value = 100
        uploadStatus.value = 'success'
        uploadText.value = '文件读取完成'
        
        setTimeout(() => {
          uploading.value = false
        }, 1000)
      }, 1000)
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
        console.log('开始解析Excel文件...', importForm.file)
        
        // 检查XLSX库是否可用
        if (typeof XLSX === 'undefined') {
          ElMessage.error('Excel解析库未加载，请刷新页面重试')
          return
        }
        
        // 检查文件类型
        if (!importForm.file.type.includes('sheet') && !importForm.file.name.endsWith('.xlsx') && !importForm.file.name.endsWith('.xls')) {
          ElMessage.error('请上传Excel文件(.xlsx或.xls格式)')
          return
        }

        // 使用FileReader读取文件
        const fileReader = new FileReader()
        
        fileReader.onload = (e) => {
          try {
            console.log('文件读取完成，开始解析...')
            const data = new Uint8Array(e.target.result)
            const workbook = XLSX.read(data, { type: 'array' })
            
            console.log('工作簿信息:', workbook.SheetNames)
            
            if (!workbook.SheetNames || workbook.SheetNames.length === 0) {
              ElMessage.error('Excel文件中没有找到工作表')
              return
            }
            
            const sheetName = workbook.SheetNames[0]
            const worksheet = workbook.Sheets[sheetName]
            
            if (!worksheet) {
              ElMessage.error('无法读取工作表内容')
              return
            }
            
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 })
            console.log('原始数据:', jsonData)
            
            // 处理表头
            if (jsonData.length === 0) {
              ElMessage.error('Excel文件为空')
              return
            }
            
            const headers = jsonData[0]
            console.log('表头:', headers)
            
            // 转换为对象数组
            const questionData = jsonData.slice(1).map(row => {
              const obj = {}
              headers.forEach((header, index) => {
                if (header) {
                  obj[header] = row[index] || ''
                }
              })
              return obj
            }).filter(row => {
              // 过滤空行
              return Object.values(row).some(value => value && value.toString().trim() !== '')
            })
            
            console.log('转换后的数据:', questionData)

            // 验证和转换数据
            previewData.value = questionData.map((row, index) => {
              const validation = validateQuestionData(row, index + 2) // +2 因为Excel从第2行开始
              return {
                ...row,
                validation
              }
            })

            console.log('预览数据:', previewData.value)
            currentStep.value = 1
            ElMessage.success('文件解析成功')
          } catch (parseError) {
            console.error('Excel解析错误:', parseError)
            ElMessage.error(`文件解析失败: ${parseError.message}`)
          }
        }
        
        fileReader.onerror = (error) => {
          console.error('文件读取错误:', error)
          ElMessage.error('文件读取失败')
        }
        
        // 读取文件
        fileReader.readAsArrayBuffer(importForm.file)
      } catch (error) {
        console.error('处理文件错误:', error)
        ElMessage.error(`处理文件失败: ${error.message}`)
      }
    }

    const validateQuestionData = (data, row) => {
      const errors = []

      try {
        console.log(`验证第${row}行数据:`, data)

        // 验证必填字段
        if (!data.题目 || (typeof data.题目 === 'string' && data.题目.trim() === '') || data.题目 === null || data.题目 === undefined) {
          errors.push('题目标题不能为空')
        }

        if (!data.题型 || !['single', 'multiple', 'judge', 'fill', 'essay'].includes(data.题型)) {
          errors.push('题型必须是：single, multiple, judge, fill, essay')
        }

        if (!data.难度 || !['easy', 'medium', 'hard'].includes(data.难度)) {
          errors.push('难度必须是：easy, medium, hard')
        }

        if (!data.答案 || (typeof data.答案 === 'string' && data.答案.trim() === '') || data.答案 === null || data.答案 === undefined) {
          errors.push('答案不能为空')
        }

        // 验证选项
        if (['single', 'multiple'].includes(data.题型)) {
          if (!data.选项 || (typeof data.选项 === 'string' && data.选项.trim() === '') || data.选项 === null || data.选项 === undefined) {
            errors.push('选择题必须提供选项')
          } else {
            // 处理选项格式（支持用|分隔的格式）
            try {
              let options
              const optionsStr = String(data.选项).trim()
              
              if (optionsStr.includes('|')) {
                // 用|分隔的格式
                options = optionsStr.split('|').map(opt => opt.trim()).filter(opt => opt)
              } else {
                // 尝试解析JSON格式
                options = JSON.parse(optionsStr)
              }
              
              if (!Array.isArray(options) || options.length < 2) {
                errors.push('选项必须是至少包含2个选项')
              }
            } catch (e) {
              errors.push('选项格式错误，请使用|分隔或JSON数组格式')
            }
          }
        }

        // 验证分值
        if (data.分值 !== undefined && data.分值 !== null && data.分值 !== '') {
          const points = parseInt(data.分值)
          if (isNaN(points) || points < 1 || points > 100) {
            errors.push('分值必须是1-100之间的整数')
          }
        }

        console.log(`第${row}行验证结果:`, { valid: errors.length === 0, errors })

        return {
          valid: errors.length === 0,
          message: errors.join('; ')
        }
      } catch (error) {
        console.error(`验证第${row}行数据时出错:`, error)
        return {
          valid: false,
          message: `数据验证出错: ${error.message}`
        }
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
          .map(item => {
            // 处理选项格式
            let options = []
            if (item.选项) {
              if (item.选项.includes('|')) {
                options = item.选项.split('|').map(opt => opt.trim()).filter(opt => opt)
              } else {
                try {
                  options = JSON.parse(item.选项)
                } catch (e) {
                  options = [item.选项]
                }
              }
            }
            
            // 处理标签
            let tags = []
            if (item.标签) {
              tags = item.标签.split('|').map(tag => tag.trim()).filter(tag => tag)
            }
            
            return {
              subject_id: importForm.subject_id,
              type: item.题型,
              title: item.题目,
              content: item.内容 || '',
              options: options,
              answer: item.答案,
              explanation: item.解析 || '',
              difficulty: item.难度,
              points: parseInt(item.分值) || 1,
              status: item.状态 || 'draft',
              tags: tags
            }
          })

        // 准备FormData格式的数据
        const formData = new FormData()
        formData.append('file', importForm.file)
        formData.append('subject_id', importForm.subject_id)
        
        console.log('发送导入请求:', {
          subject_id: importForm.subject_id,
          file: importForm.file.name,
          validDataCount: validData.length
        })

        // 调用导入API
        const result = await questionApi.importQuestions(formData)

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

    const formatOptions = (options) => {
      if (!options) return '-'
      
      try {
        let optionList
        const optionsStr = String(options).trim()
        
        if (optionsStr.includes('|')) {
          // 用|分隔的格式
          optionList = optionsStr.split('|').map(opt => opt.trim()).filter(opt => opt)
        } else {
          // 尝试解析JSON格式
          optionList = JSON.parse(optionsStr)
        }
        
        if (Array.isArray(optionList)) {
          return optionList.map((opt, index) => `${String.fromCharCode(65 + index)}. ${opt}`).join('; ')
        }
        
        return optionsStr
      } catch (e) {
        return optionsStr || '-'
      }
    }

    // 组件挂载时的调试信息
    debugExcelParsing()

    return {
      uploadRef,
      currentStep,
      importing,
      uploading,
      uploadProgress,
      uploadStatus,
      uploadText,
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
      getStatusTagType,
      formatOptions
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

:deep(.el-upload__file-list) {
  margin-top: 15px;
}

:deep(.el-upload-list__item-name) {
  max-width: none !important;
  width: 100% !important;
  word-break: break-all;
  white-space: normal;
  line-height: 1.4;
  padding: 8px 12px;
  overflow: visible !important;
  text-overflow: unset !important;
}

:deep(.el-upload-list__item-content) {
  width: 100% !important;
  max-width: none !important;
}

:deep(.el-upload-list__item) {
  width: 100% !important;
  margin-bottom: 8px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  background-color: #f8f9fa;
}

:deep(.el-upload-list__item .el-upload-list__item-info) {
  width: calc(100% - 30px) !important;
  max-width: none !important;
  flex: 1 !important;
}

:deep(.el-upload-list__item .el-upload-list__item-name) {
  max-width: none !important;
  width: 100% !important;
  overflow: visible !important;
  text-overflow: unset !important;
  white-space: normal !important;
  word-break: break-all !important;
  line-height: 1.4 !important;
  display: block !important;
  min-width: 0 !important;
}

:deep(.el-upload-list__item .el-upload-list__item-name span) {
  max-width: none !important;
  width: 100% !important;
  overflow: visible !important;
  text-overflow: unset !important;
  white-space: normal !important;
  word-break: break-all !important;
}

:deep(.el-upload-list__item:hover) {
  background-color: #f0f2f5;
}

:deep(.el-steps) {
  margin-bottom: 30px;
}

.options-display {
  font-size: 12px;
  line-height: 1.4;
  color: #606266;
  word-break: break-all;
}

.no-options {
  color: #c0c4cc;
  font-style: italic;
}

.error-text {
  color: #f56c6c;
  font-size: 12px;
}

.success-text {
  color: #67c23a;
  font-size: 12px;
}

.upload-progress {
  margin-top: 15px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.upload-text {
  margin: 8px 0 0 0;
  text-align: center;
  color: #666;
  font-size: 14px;
}
</style>
