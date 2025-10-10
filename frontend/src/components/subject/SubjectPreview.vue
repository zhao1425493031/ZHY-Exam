<template>
  <div class="subject-preview">
    <div class="subject-header">
      <div class="subject-title">
        <h2>{{ subject.name }}</h2>
        <div class="subject-meta">
          <el-tag :type="getStatusTagType(subject.status)" size="small">
            {{ getStatusLabel(subject.status) }}
          </el-tag>
          <el-tag :type="subject.is_free ? 'success' : 'warning'" size="small">
            {{ subject.is_free ? '免费' : '收费' }}
          </el-tag>
          <span class="subject-code">{{ subject.code }}</span>
        </div>
      </div>
      <div class="subject-price" v-if="!subject.is_free">
        <div class="price-current">¥{{ subject.price }}</div>
        <div v-if="subject.original_price > subject.price" class="price-original">
          ¥{{ subject.original_price }}
        </div>
        <div class="discount-rate">{{ subject.discount_rate }}%</div>
      </div>
    </div>

    <div class="subject-content">
      <div v-if="subject.category" class="subject-category">
        <h4>分类</h4>
        <p>{{ subject.category }}</p>
      </div>

      <div v-if="subject.description" class="subject-description">
        <h4>描述</h4>
        <p>{{ subject.description }}</p>
      </div>

      <div class="subject-info">
        <h4>基本信息</h4>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">科目代码：</span>
            <span class="info-value">{{ subject.code }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">科目名称：</span>
            <span class="info-value">{{ subject.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">分类：</span>
            <span class="info-value">{{ subject.category || '未设置' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">状态：</span>
            <span class="info-value">
              <el-tag :type="getStatusTagType(subject.status)" size="small">
                {{ getStatusLabel(subject.status) }}
              </el-tag>
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">收费类型：</span>
            <span class="info-value">
              <el-tag :type="subject.is_free ? 'success' : 'warning'" size="small">
                {{ subject.is_free ? '免费' : '收费' }}
              </el-tag>
            </span>
          </div>
          <div v-if="!subject.is_free" class="info-item">
            <span class="info-label">价格：</span>
            <span class="info-value price-text">¥{{ subject.price }}</span>
          </div>
        </div>
      </div>

      <div v-if="!subject.is_free" class="pricing-details">
        <h4>价格详情</h4>
        <div class="pricing-grid">
          <div class="pricing-item">
            <span class="pricing-label">原价：</span>
            <span class="pricing-value original">¥{{ subject.original_price }}</span>
          </div>
          <div class="pricing-item">
            <span class="pricing-label">折扣率：</span>
            <span class="pricing-value">{{ subject.discount_rate }}%</span>
          </div>
          <div class="pricing-item">
            <span class="pricing-label">现价：</span>
            <span class="pricing-value current">¥{{ subject.price }}</span>
          </div>
          <div class="pricing-item">
            <span class="pricing-label">节省：</span>
            <span class="pricing-value save">¥{{ (subject.original_price - subject.price).toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'SubjectPreview',
  props: {
    subject: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    // 工具方法
    const getStatusLabel = (status) => {
      const labels = {
        active: '启用',
        inactive: '禁用'
      }
      return labels[status] || status
    }

    const getStatusTagType = (status) => {
      const types = {
        active: 'success',
        inactive: 'danger'
      }
      return types[status] || 'default'
    }

    return {
      getStatusLabel,
      getStatusTagType
    }
  }
}
</script>

<style scoped>
.subject-preview {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.subject-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.subject-title h2 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.subject-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.subject-code {
  color: #909399;
  font-size: 14px;
  font-family: monospace;
}

.subject-price {
  text-align: right;
}

.price-current {
  font-size: 24px;
  font-weight: 600;
  color: #e6a23c;
}

.price-original {
  font-size: 16px;
  color: #909399;
  text-decoration: line-through;
  margin-top: 5px;
}

.discount-rate {
  font-size: 14px;
  color: #67c23a;
  font-weight: 500;
  margin-top: 5px;
}

.subject-content {
  line-height: 1.6;
}

.subject-content h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 500;
}

.subject-category,
.subject-description {
  margin-bottom: 25px;
}

.subject-category p,
.subject-description p {
  margin: 0;
  color: #606266;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.subject-info,
.pricing-details {
  margin-bottom: 25px;
}

.info-grid,
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item,
.pricing-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.info-label,
.pricing-label {
  color: #606266;
  font-weight: 500;
}

.info-value,
.pricing-value {
  color: #303133;
}

.price-text {
  color: #e6a23c;
  font-weight: 600;
}

.pricing-value.original {
  color: #909399;
  text-decoration: line-through;
}

.pricing-value.current {
  color: #e6a23c;
  font-weight: 600;
}

.pricing-value.save {
  color: #67c23a;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .subject-preview {
    padding: 15px;
  }
  
  .subject-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .subject-price {
    text-align: left;
  }
  
  .info-grid,
  .pricing-grid {
    grid-template-columns: 1fr;
  }
}
</style>
