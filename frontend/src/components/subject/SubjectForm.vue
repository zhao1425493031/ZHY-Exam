<template>
  <div class="subject-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
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
              placeholder="请输入科目代码"
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

      <el-divider content-position="left">收费设置</el-divider>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="收费类型" prop="is_free">
            <el-radio-group v-model="form.is_free" @change="handleFreeChange">
              <el-radio :label="true">免费</el-radio>
              <el-radio :label="false">收费</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="8" v-if="!form.is_free">
          <el-form-item label="价格" prop="price">
            <el-input-number
              v-model="form.price"
              :min="0"
              :max="9999.99"
              :precision="2"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8" v-if="!form.is_free">
          <el-form-item label="原价" prop="original_price">
            <el-input-number
              v-model="form.original_price"
              :min="0"
              :max="9999.99"
              :precision="2"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20" v-if="!form.is_free">
        <el-col :span="8">
          <el-form-item label="折扣率" prop="discount_rate">
            <el-input-number
              v-model="form.discount_rate"
              :min="0"
              :max="100"
              :precision="2"
              style="width: 100%"
            />
            <span class="form-tip">%</span>
          </el-form-item>
        </el-col>
        <el-col :span="16">
          <div class="price-preview">
            <div class="price-item">
              <span class="label">原价：</span>
              <span class="value">¥{{ form.original_price || 0 }}</span>
            </div>
            <div class="price-item">
              <span class="label">折扣率：</span>
              <span class="value">{{ form.discount_rate || 100 }}%</span>
            </div>
            <div class="price-item">
              <span class="label">现价：</span>
              <span class="value price-current">¥{{ calculatedPrice }}</span>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ subject ? '更新' : '创建' }}
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
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import SubjectPreview from '@/components/subject/SubjectPreview.vue'

export default {
  name: 'SubjectForm',
  components: {
    SubjectPreview
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

    // 表单数据
    const form = reactive({
      name: '',
      code: '',
      category: '',
      description: '',
      status: 'active',
      is_free: true,
      price: 0.00,
      original_price: 0.00,
      discount_rate: 100.00
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
        { pattern: /^[a-zA-Z0-9_-]+$/, message: '科目代码只能包含字母、数字、下划线和连字符', trigger: 'blur' }
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
        { type: 'number', min: 0, max: 9999.99, message: '价格必须在0-9999.99之间', trigger: 'blur' }
      ],
      original_price: [
        { type: 'number', min: 0, max: 9999.99, message: '原价必须在0-9999.99之间', trigger: 'blur' }
      ],
      discount_rate: [
        { type: 'number', min: 0, max: 100, message: '折扣率必须在0-100之间', trigger: 'blur' }
      ]
    }

    // 计算属性
    const calculatedPrice = computed(() => {
      if (form.is_free) return 0
      if (!form.original_price || !form.discount_rate) return 0
      return (form.original_price * form.discount_rate / 100).toFixed(2)
    })

    // 方法
    const handleFreeChange = (isFree) => {
      if (isFree) {
        form.price = 0
        form.original_price = 0
        form.discount_rate = 100
      } else {
        form.price = 0
        form.original_price = 0
        form.discount_rate = 100
      }
    }

    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        
        // 计算实际价格
        if (!form.is_free) {
          form.price = parseFloat(calculatedPrice.value)
        } else {
          form.price = 0
          form.original_price = 0
          form.discount_rate = 100
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

    // 监听价格变化，自动计算折扣率
    watch([() => form.price, () => form.original_price], ([price, originalPrice]) => {
      if (!form.is_free && originalPrice > 0 && price > 0) {
        form.discount_rate = ((price / originalPrice) * 100).toFixed(2)
      }
    })

    // 监听折扣率变化，自动计算价格
    watch([() => form.discount_rate, () => form.original_price], ([discountRate, originalPrice]) => {
      if (!form.is_free && originalPrice > 0 && discountRate > 0) {
        form.price = (originalPrice * discountRate / 100).toFixed(2)
      }
    })

    // 初始化表单数据
    const initForm = () => {
      if (props.subject) {
        Object.assign(form, props.subject)
        
        // 确保数值类型
        form.price = parseFloat(form.price) || 0
        form.original_price = parseFloat(form.original_price) || 0
        form.discount_rate = parseFloat(form.discount_rate) || 100
      }
    }

    // 组件挂载时初始化
    initForm()

    return {
      formRef,
      submitting,
      showPreview,
      form,
      rules,
      calculatedPrice,
      handleFreeChange,
      handleSubmit,
      handleCancel,
      handlePreview
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

.price-preview {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.price-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.price-item:last-child {
  margin-bottom: 0;
}

.price-item .label {
  color: #606266;
  font-weight: 500;
}

.price-item .value {
  color: #303133;
}

.price-current {
  color: #e6a23c;
  font-weight: 600;
  font-size: 16px;
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
