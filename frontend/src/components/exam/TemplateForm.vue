<template>
  <div class="template-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
    >
      <el-form-item label="模板名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入模板名称" />
      </el-form-item>
      
      <el-form-item label="模板描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入模板描述"
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
      
      <el-form-item label="模板配置" prop="template_config">
        <el-input
          v-model="templateConfigJson"
          type="textarea"
          :rows="6"
          placeholder="请输入模板配置JSON"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'TemplateForm',
  props: {
    template: {
      type: Object,
      default: () => ({})
    },
    subjects: {
      type: Array,
      default: () => []
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const formRef = ref()
    
    const form = reactive({
      name: '',
      description: '',
      subject_id: null,
      template_config: {}
    })
    
    const rules = {
      name: [
        { required: true, message: '请输入模板名称', trigger: 'blur' }
      ],
      subject_id: [
        { required: true, message: '请选择科目', trigger: 'change' }
      ]
    }
    
    // 模板配置JSON字符串
    const templateConfigJson = computed({
      get() {
        return JSON.stringify(form.template_config, null, 2)
      },
      set(value) {
        try {
          form.template_config = JSON.parse(value)
        } catch (e) {
          console.error('JSON解析错误:', e)
        }
      }
    })
    
    // 监听props变化
    watch(() => props.template, (newTemplate) => {
      if (newTemplate && Object.keys(newTemplate).length > 0) {
        Object.assign(form, newTemplate)
      }
    }, { immediate: true })
    
    const handleSubmit = async () => {
      try {
        await formRef.value.validate()
        emit('submit', { ...form })
        ElMessage.success('保存成功')
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }
    
    const handleCancel = () => {
      emit('cancel')
    }
    
    return {
      formRef,
      form,
      rules,
      templateConfigJson,
      handleSubmit,
      handleCancel
    }
  }
}
</script>

<style scoped>
.template-form {
  padding: 20px;
}
</style>
