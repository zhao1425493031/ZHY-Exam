<template>
  <div class="template-use">
    <el-dialog
      v-model="visible"
      title="使用考试模板"
      width="600px"
      @close="handleClose"
    >
      <div class="template-info">
        <h4>{{ template.name }}</h4>
        <p>{{ template.description }}</p>
      </div>
      
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
      </el-form>
      
      <template #footer>
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit">创建考试</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'TemplateUse',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    template: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['update:modelValue', 'submit'],
  setup(props, { emit }) {
    const formRef = ref()
    
    const visible = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value)
    })
    
    const form = reactive({
      title: '',
      description: '',
      duration: 120,
      start_time: '',
      end_time: ''
    })
    
    const rules = {
      title: [
        { required: true, message: '请输入考试标题', trigger: 'blur' }
      ],
      duration: [
        { required: true, message: '请输入考试时长', trigger: 'blur' }
      ]
    }
    
    // 监听模板变化，设置默认值
    watch(() => props.template, (newTemplate) => {
      if (newTemplate && Object.keys(newTemplate).length > 0) {
        form.title = `${newTemplate.name} - 考试`
        form.description = newTemplate.description
      }
    }, { immediate: true })
    
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        
        const examData = {
          ...form,
          subject_id: props.template.subject_id,
          template_id: props.template.id,
          template_config: props.template.template_config
        }
        
        emit('submit', examData)
        ElMessage.success('考试创建成功')
        handleClose()
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }
    
    const handleClose = () => {
      visible.value = false
      // 重置表单
      Object.assign(form, {
        title: '',
        description: '',
        duration: 120,
        start_time: '',
        end_time: ''
      })
    }
    
    return {
      formRef,
      visible,
      form,
      rules,
      handleSubmit,
      handleClose
    }
  }
}
</script>

<style scoped>
.template-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.template-info h4 {
  margin: 0 0 10px 0;
  color: #409eff;
}

.template-info p {
  margin: 0;
  color: #666;
}
</style>
