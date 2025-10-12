<template>
  <div class="subject-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      @submit.prevent="handleSubmit"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="科目名称" prop="name">
            <el-input
              v-model="form.name"
              placeholder="请输入科目名称"
              maxlength="100"
              show-word-limit
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="科目代码" prop="code">
            <el-input
              v-model="form.code"
              placeholder="请输入科目代码（大写字母、数字、下划线）"
              maxlength="20"
              show-word-limit
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="分类" prop="category">
            <el-input
              v-model="form.category"
              placeholder="请输入科目分类"
              maxlength="50"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="状态" prop="status">
            <el-select
              v-model="form.status"
              placeholder="请选择状态"
              style="width: 100%"
            >
              <el-option label="启用" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入科目描述"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="课程封面" prop="cover_image">
        <div class="image-upload-wrapper">
          <ImageUpload
            v-model="form.cover_image"
            :preview-alt="form.name || '课程封面'"
            @upload-success="handleImageUploadSuccess"
            @upload-error="handleImageUploadError"
          />
        </div>
        <div class="form-item-tip">
          <el-icon><InfoFilled /></el-icon>
          支持 JPG、PNG、GIF 格式，建议尺寸 300×200px，文件大小不超过 2MB
        </div>
      </el-form-item>

      <el-divider content-position="left">收费设置</el-divider>

      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="收费类型" prop="is_free">
            <el-radio-group v-model="form.is_free" @change="handleFreeChange">
              <el-radio :value="true">免费</el-radio>
              <el-radio :value="false">收费</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>

      <template v-if="!form.is_free">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="原价" prop="original_price">
              <el-input-number
                v-model="form.original_price"
                :min="0"
                :max="99999.99"
                :precision="2"
                :step="10"
                style="width: 100%"
                placeholder="输入原价"
                @change="handleOriginalPriceChange"
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="折扣率" prop="discount_rate">
              <el-input-number
                v-model="form.discount_rate"
                :min="1"
                :max="100"
                :precision="0"
                :step="5"
                style="width: 100%"
                placeholder="输入折扣率"
                @change="handleDiscountRateChange"
              >
                <template #suffix>%</template>
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="现价" prop="price">
              <el-input-number
                v-model="form.price"
                :min="0"
                :max="99999.99"
                :precision="2"
                :step="10"
                style="width: 100%"
                placeholder="自动计算"
                :disabled="true"
                readonly
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-alert
              :title="priceCalculationTip"
              type="info"
              :closable="false"
              show-icon
            >
              <template #default>
                <div class="price-calculation-info">
                  <p><strong>计算规则：</strong></p>
                  <ul>
                    <li>修改 <strong>原价</strong> 或 <strong>折扣率</strong> → 自动计算 <strong>现价</strong></li>
                    <li>现价为只读字段，根据原价和折扣率自动计算</li>
                    <li>公式：现价 = 原价 × (折扣率 / 100)</li>
                  </ul>
                  <div class="price-preview-box">
                    <div class="preview-item">
                      <span class="label">原价：</span>
                      <span class="value">¥{{ formatPrice(form.original_price) }}</span>
                    </div>
                    <div class="preview-item">
                      <span class="label">×</span>
                      <span class="value">{{ form.discount_rate }}%</span>
                    </div>
                    <div class="preview-item">
                      <span class="label">=</span>
                      <span class="value price-highlight">¥{{ formatPrice(form.price) }}</span>
                    </div>
                    <div class="preview-item savings" v-if="form.original_price > form.price">
                      <span class="label">节省：</span>
                      <span class="value">¥{{ formatPrice(form.original_price - form.price) }}</span>
                    </div>
                  </div>
                </div>
              </template>
            </el-alert>
          </el-col>
        </el-row>
      </template>

      <el-form-item style="margin-top: 24px;">
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ subject ? '更新科目' : '创建科目' }}
        </el-button>
        <el-button @click="handleCancel">取消</el-button>
        <el-button v-if="subject" @click="handlePreview">预览</el-button>
      </el-form-item>
    </el-form>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="showPreview"
      title="科目预览"
      width="50%"
    >
      <SubjectPreview
        v-if="showPreview"
        :subject="form"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'
import SubjectPreview from '@/components/subject/SubjectPreview.vue'
import ImageUpload from '@/components/common/ImageUpload.vue'

export default {
  name: 'SubjectForm',
  components: {
    SubjectPreview,
    ImageUpload,
    InfoFilled
  },
  props: {
    subject: {
      type: Object,
      default: null
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const formRef = ref()
    const submitting = ref(false)
    const showPreview = ref(false)
    
    // 用于防止循环计算的标志
    const isCalculating = ref(false)

    // 表单数据
    const form = reactive({
      name: '',
      code: '',
      category: '',
      description: '',
      cover_image: '',
      status: 'active',
      is_free: true,
      price: 0.00,
      original_price: 0.00,
      discount_rate: 100
    })

    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入科目名称', trigger: 'blur' },
        { min: 2, message: '科目名称至少2个字符', trigger: 'blur' },
        { max: 100, message: '科目名称不能超过100个字符', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入科目代码', trigger: 'blur' },
        { min: 2, message: '科目代码至少2个字符', trigger: 'blur' },
        { max: 20, message: '科目代码不能超过20个字符', trigger: 'blur' },
        { pattern: /^[A-Z0-9_]+$/, message: '科目代码只能包含大写字母、数字、下划线', trigger: 'blur' }
      ],
      category: [
        { max: 50, message: '分类不能超过50个字符', trigger: 'blur' }
      ],
      description: [
        { max: 500, message: '描述不能超过500个字符', trigger: 'blur' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ],
      price: [
        { required: true, message: '请输入价格', trigger: 'blur' },
        { type: 'number', min: 0, max: 99999.99, message: '价格必须在0-99999.99之间', trigger: 'blur' }
      ],
      original_price: [
        { required: true, message: '请输入原价', trigger: 'blur' },
        { type: 'number', min: 0, max: 99999.99, message: '原价必须在0-99999.99之间', trigger: 'blur' }
      ],
      discount_rate: [
        { required: true, message: '请输入折扣率', trigger: 'blur' },
        { type: 'number', min: 1, max: 100, message: '折扣率必须在1-100之间', trigger: 'blur' }
      ]
    }

    // 计算提示信息
    const priceCalculationTip = computed(() => {
      if (form.is_free) return '免费科目无需设置价格'
      
      const originalPrice = parseFloat(form.original_price) || 0
      const discountRate = parseFloat(form.discount_rate) || 100
      const price = parseFloat(form.price) || 0
      
      if (originalPrice === 0) return '请先输入原价'
      if (discountRate === 100) return '无折扣，现价等于原价'
      
      const calculatedPrice = (originalPrice * discountRate / 100).toFixed(2)
      const savings = (originalPrice - price).toFixed(2)
      
      return `折扣后价格：¥${calculatedPrice}，节省：¥${savings}`
    })

    // 格式化价格显示
    const formatPrice = (price) => {
      return parseFloat(price || 0).toFixed(2)
    }

    // 方法：处理免费/收费切换
    const handleFreeChange = (isFree) => {
      if (isFree) {
        form.price = 0
        form.original_price = 0
        form.discount_rate = 100
      } else {
        // 切换到收费时，设置默认值
        if (form.original_price === 0) {
          form.original_price = 100
        }
        if (form.discount_rate === 0) {
          form.discount_rate = 100
        }
        // 自动计算现价
        calculatePrice()
      }
    }

    // 方法：当原价或折扣率改变时，自动计算现价
    const calculatePrice = () => {
      if (isCalculating.value) return
      
      isCalculating.value = true
      
      const originalPrice = parseFloat(form.original_price) || 0
      const discountRate = parseFloat(form.discount_rate) || 100
      
      if (originalPrice > 0 && discountRate > 0) {
        form.price = parseFloat((originalPrice * discountRate / 100).toFixed(2))
      } else {
        form.price = 0
      }
      
      setTimeout(() => {
        isCalculating.value = false
      }, 100)
    }


    // 事件处理器
    const handleOriginalPriceChange = (value) => {
      if (form.is_free || !value || value === 0) return
      calculatePrice()
    }

    const handleDiscountRateChange = (value) => {
      if (form.is_free || !value) return
      if (value < 1) {
        form.discount_rate = 1
      } else if (value > 100) {
        form.discount_rate = 100
      }
      calculatePrice()
    }


    // 提交表单
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        
        // 验证价格逻辑
        if (!form.is_free) {
          if (parseFloat(form.original_price) <= 0) {
            ElMessage.error('原价必须大于0')
            return
          }
          
          if (parseFloat(form.price) > parseFloat(form.original_price)) {
            ElMessage.error('现价不能高于原价')
            return
          }
          
          if (parseFloat(form.discount_rate) < 1 || parseFloat(form.discount_rate) > 100) {
            ElMessage.error('折扣率必须在1-100之间')
            return
          }
          
          // 确保价格精度
          form.price = parseFloat(form.price).toFixed(2)
          form.original_price = parseFloat(form.original_price).toFixed(2)
          form.discount_rate = Math.round(parseFloat(form.discount_rate))
        } else {
          // 免费科目，清空价格信息
          form.price = 0
          form.original_price = 0
          form.discount_rate = 100
        }

        submitting.value = true
        emit('submit', { ...form })
      } catch (error) {
        console.error('Form validation error:', error)
        ElMessage.error('表单验证失败，请检查输入')
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

    // 初始化表单数据
    const initForm = () => {
      if (props.subject) {
        Object.assign(form, props.subject)
        
        // 确保数值类型和精度
        form.price = parseFloat(form.price) || 0
        form.original_price = parseFloat(form.original_price) || 0
        form.discount_rate = parseInt(form.discount_rate) || 100
        
        // 如果是免费科目
        if (form.is_free) {
          form.price = 0
          form.original_price = 0
          form.discount_rate = 100
        }
      }
    }

    // 组件挂载时初始化
    initForm()

    // 图片上传成功处理
    const handleImageUploadSuccess = (imageUrl) => {
      console.log('图片上传成功:', imageUrl)
    }

    // 图片上传失败处理
    const handleImageUploadError = (error) => {
      console.error('图片上传失败:', error)
    }

    return {
      formRef,
      submitting,
      showPreview,
      form,
      rules,
      priceCalculationTip,
      formatPrice,
      handleFreeChange,
      handleOriginalPriceChange,
      handleDiscountRateChange,
      handleSubmit,
      handleCancel,
      handlePreview,
      handleImageUploadSuccess,
      handleImageUploadError
    }
  }
}
</script>

<style scoped>
.subject-form {
  padding: 20px;
}

.form-tip {
  margin-left: 5px;
  color: #909399;
  font-size: 14px;
}

.price-calculation-info {
  p {
    margin: 0 0 12px 0;
    font-size: 15px;
    color: #606266;
  }
  
  ul {
    margin: 0 0 16px 0;
    padding-left: 24px;
    
    li {
      margin-bottom: 8px;
      font-size: 14px;
      color: #606266;
      line-height: 1.6;
      
      strong {
        color: #409eff;
        font-weight: 600;
      }
    }
  }
}

.price-preview-box {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  border-radius: 12px;
  border: 2px solid #409eff;
  
  .preview-item {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .label {
      font-size: 14px;
      color: #606266;
      font-weight: 500;
    }
    
    .value {
      font-size: 18px;
      color: #303133;
      font-weight: 700;
    }
    
    &.savings {
      margin-left: auto;
      padding: 8px 16px;
      background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
      border-radius: 8px;
      
      .label, .value {
        color: white;
        font-size: 15px;
      }
    }
  }
  
  .price-highlight {
    color: #e6a23c;
    font-size: 22px;
    font-weight: 800;
  }
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #303133;
}

:deep(.el-textarea__inner) {
  resize: vertical;
}

:deep(.el-divider__text) {
  font-weight: 600;
  color: #409eff;
  font-size: 16px;
}

:deep(.el-input-number) {
  width: 100%;
  
  .el-input__wrapper {
    border-radius: 8px;
  }
  
  .el-input__inner {
    text-align: left;
    font-weight: 500;
  }
  
  &.is-disabled {
    .el-input__wrapper {
      background-color: #f5f7fa;
      border-color: #e4e7ed;
      
      .el-input__inner {
        color: #606266;
        cursor: not-allowed;
      }
    }
  }
}

:deep(.el-alert) {
  border-radius: 12px;
  padding: 16px;
  
  .el-alert__content {
    width: 100%;
  }
}

:deep(.el-radio-group) {
  .el-radio {
    margin-right: 24px;
    
    .el-radio__label {
      font-weight: 500;
      font-size: 15px;
    }
  }
}

.image-upload-wrapper {
  width: fit-content;
  margin-bottom: 8px;
}

.form-item-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  
  .el-icon {
    font-size: 14px;
  }
}
</style>
