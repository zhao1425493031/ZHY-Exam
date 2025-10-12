<template>
  <div class="image-upload">
    <div class="upload-area" 
         :class="{ 'dragover': isDragOver, 'has-image': previewUrl }"
         @click="triggerUpload"
         @dragover.prevent="handleDragOver"
         @dragleave.prevent="handleDragLeave"
         @drop.prevent="handleDrop">
      
      <!-- 预览图片 -->
      <div v-if="previewUrl" class="preview-container">
        <img :src="previewUrl" :alt="previewAlt" class="preview-image" />
        <div class="preview-overlay">
          <el-button type="primary" size="small" @click.stop="triggerUpload">
            <el-icon><Edit /></el-icon>
            更换图片
          </el-button>
          <el-button type="danger" size="small" @click.stop="removeImage">
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </div>
      </div>
      
      <!-- 上传提示 -->
      <div v-else class="upload-tip">
        <div class="upload-icon">
          <el-icon size="48"><Upload /></el-icon>
        </div>
        <div class="upload-text">
          <p class="upload-title">点击或拖拽上传图片</p>
          <p class="upload-subtitle">支持 JPG、PNG、GIF 格式，大小不超过 2MB</p>
          <p class="upload-size">建议尺寸：300×200px</p>
        </div>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="uploading" class="upload-loading">
        <el-progress type="circle" :percentage="uploadProgress" />
        <p>上传中...</p>
      </div>
    </div>
    
    <!-- 隐藏的文件输入 -->
    <input 
      ref="fileInput"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleFileSelect"
    />
    
    <!-- 错误提示 -->
    <div v-if="errorMessage" class="error-message">
      <el-icon><Warning /></el-icon>
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Edit, Delete, Warning } from '@element-plus/icons-vue'

export default {
  name: 'ImageUpload',
  components: {
    Upload,
    Edit,
    Delete,
    Warning
  },
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    previewAlt: {
      type: String,
      default: '预览图片'
    },
    maxSize: {
      type: Number,
      default: 2 * 1024 * 1024 // 2MB
    },
    acceptedTypes: {
      type: Array,
      default: () => ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    }
  },
  emits: ['update:modelValue', 'upload-success', 'upload-error'],
  setup(props, { emit }) {
    const fileInput = ref(null)
    const isDragOver = ref(false)
    const uploading = ref(false)
    const uploadProgress = ref(0)
    const errorMessage = ref('')
    
    // 预览URL
    const previewUrl = computed(() => {
      console.log('预览URL计算 - modelValue:', props.modelValue)
      if (props.modelValue) {
        // 如果是完整的URL，直接使用
        if (props.modelValue.startsWith('http')) {
          console.log('使用完整URL:', props.modelValue)
          return props.modelValue
        }
        // 如果是相对路径，直接使用（前端代理会处理）
        const finalUrl = props.modelValue.startsWith('/') ? props.modelValue : `/${props.modelValue}`
        console.log('使用相对路径（通过代理）:', finalUrl)
        return finalUrl
      }
      console.log('没有modelValue，返回空字符串')
      return ''
    })
    
    // 触发文件选择
    const triggerUpload = () => {
      if (uploading.value) return
      fileInput.value?.click()
    }
    
    // 处理文件选择
    const handleFileSelect = (event) => {
      const file = event.target.files?.[0]
      if (file) {
        validateAndUpload(file)
      }
    }
    
    // 处理拖拽悬停
    const handleDragOver = (event) => {
      event.preventDefault()
      isDragOver.value = true
    }
    
    // 处理拖拽离开
    const handleDragLeave = (event) => {
      event.preventDefault()
      isDragOver.value = false
    }
    
    // 处理文件拖放
    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      
      const files = event.dataTransfer.files
      if (files.length > 0) {
        validateAndUpload(files[0])
      }
    }
    
    // 验证并上传文件
    const validateAndUpload = async (file) => {
      errorMessage.value = ''
      
      // 验证文件类型
      if (!props.acceptedTypes.includes(file.type)) {
        errorMessage.value = `不支持的文件格式，请选择 ${props.acceptedTypes.map(type => type.split('/')[1].toUpperCase()).join('、')} 格式的图片`
        return
      }
      
      // 验证文件大小
      if (file.size > props.maxSize) {
        errorMessage.value = `文件大小不能超过 ${(props.maxSize / 1024 / 1024).toFixed(1)}MB`
        return
      }
      
      try {
        uploading.value = true
        uploadProgress.value = 0
        
        // 模拟上传进度
        const progressInterval = setInterval(() => {
          if (uploadProgress.value < 90) {
            uploadProgress.value += 10
          }
        }, 100)
        
        // 创建FormData
        const formData = new FormData()
        formData.append('file', file)
        formData.append('type', 'subject_cover')
        
        // 获取token
        const token = localStorage.getItem('token')
        if (!token) {
          throw new Error('请先登录')
        }
        
        // 上传文件
        const response = await fetch('/api/files/upload', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })
        
        clearInterval(progressInterval)
        uploadProgress.value = 100
        
        if (response.ok) {
          const result = await response.json()
          console.log('上传响应:', result)
          if (result.code === 200) {
            const imageUrl = result.data.file_path || result.data.url || result.data
            console.log('获取到的图片URL:', imageUrl)
            emit('update:modelValue', imageUrl)
            emit('upload-success', imageUrl)
            ElMessage.success('图片上传成功')
          } else {
            throw new Error(result.message || '上传失败')
          }
        } else {
          throw new Error('上传失败')
        }
      } catch (error) {
        console.error('上传失败:', error)
        errorMessage.value = error.message || '上传失败，请重试'
        emit('upload-error', error)
        ElMessage.error(errorMessage.value)
      } finally {
        uploading.value = false
        uploadProgress.value = 0
      }
    }
    
    // 删除图片
    const removeImage = () => {
      emit('update:modelValue', '')
      emit('upload-success', '')
      ElMessage.success('图片已删除')
    }
    
    // 监听modelValue变化，清除错误信息
    watch(() => props.modelValue, () => {
      if (props.modelValue) {
        errorMessage.value = ''
      }
    })
    
    return {
      fileInput,
      isDragOver,
      uploading,
      uploadProgress,
      errorMessage,
      previewUrl,
      triggerUpload,
      handleFileSelect,
      handleDragOver,
      handleDragLeave,
      handleDrop,
      removeImage
    }
  }
}
</script>

<style lang="scss" scoped>
.image-upload {
  width: 100%;
}

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
  min-height: 150px;
  max-width: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  
  &:hover {
    border-color: #409eff;
    background: #f0f9ff;
  }
  
  &.dragover {
    border-color: #409eff;
    background: #e6f7ff;
  }
  
  &.has-image {
    padding: 0;
    min-height: 150px;
    border-style: solid;
    border-color: #d9d9d9;
  }
}

.preview-container {
  position: relative;
  width: 100%;
  height: 150px;
  overflow: hidden;
  border-radius: 6px;
  
  .preview-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .preview-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover .preview-overlay {
    opacity: 1;
  }
}

.upload-tip {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  color: #c0c4cc;
  transition: color 0.3s ease;
}

.upload-area:hover .upload-icon {
  color: #409eff;
}

.upload-text {
  .upload-title {
    font-size: 1rem;
    color: #606266;
    margin: 0 0 0.5rem 0;
    font-weight: 500;
  }
  
  .upload-subtitle {
    font-size: 0.875rem;
    color: #909399;
    margin: 0 0 0.25rem 0;
  }
  
  .upload-size {
    font-size: 0.75rem;
    color: #c0c4cc;
    margin: 0;
  }
}

.upload-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  
  p {
    margin: 1rem 0 0 0;
    color: #606266;
    font-size: 0.875rem;
  }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #f56c6c;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: #fef0f0;
  border: 1px solid #fbc4c4;
  border-radius: 4px;
}

// 响应式设计
@media (max-width: 768px) {
  .upload-area {
    padding: 1rem;
    min-height: 120px;
    max-width: 250px;
  }
  
  .preview-container {
    height: 120px;
  }
  
  .upload-tip {
    gap: 0.5rem;
  }
  
  .upload-icon {
    font-size: 2rem;
  }
  
  .upload-text {
    .upload-title {
      font-size: 0.875rem;
    }
    
    .upload-subtitle {
      font-size: 0.75rem;
    }
    
    .upload-size {
      font-size: 0.625rem;
    }
  }
}
</style>
