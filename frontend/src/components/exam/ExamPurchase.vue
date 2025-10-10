<template>
  <div class="exam-purchase">
    <div class="purchase-header">
      <h3>{{ exam.title }}</h3>
      <div class="exam-info">
        <span>{{ exam.question_count }}题 | {{ exam.total_points }}分 | {{ formatDuration(exam.duration) }}</span>
      </div>
    </div>

    <div class="purchase-content">
      <!-- 价格信息 -->
      <div class="price-section">
        <div class="price-display">
          <div class="price-current">
            <span class="price-label">现价：</span>
            <span class="price-value">¥{{ examPrice }}</span>
          </div>
          <div v-if="originalPrice > examPrice" class="price-original">
            <span class="price-label">原价：</span>
            <span class="price-value">¥{{ originalPrice }}</span>
          </div>
        </div>
        
        <div v-if="discountRate < 100" class="discount-info">
          <el-tag type="success" size="small">
            优惠 {{ 100 - discountRate }}%
          </el-tag>
        </div>
      </div>

      <!-- 优惠券 -->
      <div class="coupon-section">
        <div class="section-title">
          <h4>优惠券</h4>
        </div>
        <div class="coupon-input">
          <el-input
            v-model="couponCode"
            placeholder="请输入优惠券代码"
            clearable
          >
            <template #append>
              <el-button @click="validateCoupon" :loading="validatingCoupon">
                验证
              </el-button>
            </template>
          </el-input>
        </div>
        <div v-if="validatedCoupon" class="coupon-info">
          <el-tag type="success">
            {{ validatedCoupon.name }} - 优惠 ¥{{ couponDiscount }}
          </el-tag>
        </div>
      </div>

      <!-- 支付方式 -->
      <div class="payment-section">
        <div class="section-title">
          <h4>支付方式</h4>
        </div>
        <div class="payment-methods">
          <div
            v-for="method in paymentMethods"
            :key="method.value"
            class="payment-method"
            :class="{ 'method-selected': selectedPaymentMethod === method.value }"
            @click="selectPaymentMethod(method.value)"
          >
            <div class="method-icon">
              <el-icon :size="24">
                <component :is="method.icon" />
              </el-icon>
            </div>
            <div class="method-info">
              <div class="method-name">{{ method.name }}</div>
              <div class="method-desc">{{ method.description }}</div>
            </div>
            <div class="method-radio">
              <el-radio :value="selectedPaymentMethod" :label="method.value" />
            </div>
          </div>
        </div>
      </div>

      <!-- 订单摘要 -->
      <div class="order-summary">
        <div class="section-title">
          <h4>订单摘要</h4>
        </div>
        <div class="summary-items">
          <div class="summary-item">
            <span class="item-label">考试费用：</span>
            <span class="item-value">¥{{ examPrice }}</span>
          </div>
          <div v-if="couponDiscount > 0" class="summary-item">
            <span class="item-label">优惠券：</span>
            <span class="item-value discount">-¥{{ couponDiscount }}</span>
          </div>
          <div class="summary-item total">
            <span class="item-label">应付金额：</span>
            <span class="item-value">¥{{ finalPrice }}</span>
          </div>
        </div>
      </div>

      <!-- 用户协议 -->
      <div class="agreement-section">
        <el-checkbox v-model="agreedToTerms">
          我已阅读并同意
          <el-link type="primary" @click="showTerms = true">《用户协议》</el-link>
          和
          <el-link type="primary" @click="showPrivacy = true">《隐私政策》</el-link>
        </el-checkbox>
      </div>
    </div>

    <div class="purchase-footer">
      <div class="footer-info">
        <span>应付金额：</span>
        <span class="final-price">¥{{ finalPrice }}</span>
      </div>
      <div class="footer-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button
          type="primary"
          @click="handlePurchase"
          :loading="purchasing"
          :disabled="!agreedToTerms || finalPrice <= 0"
        >
          立即购买
        </el-button>
      </div>
    </div>

    <!-- 用户协议对话框 -->
    <el-dialog v-model="showTerms" title="用户协议" width="60%">
      <div class="terms-content">
        <h4>1. 服务条款</h4>
        <p>用户购买考试服务后，可在规定时间内参加考试。</p>
        
        <h4>2. 退款政策</h4>
        <p>考试开始前24小时内可申请退款，考试开始后不支持退款。</p>
        
        <h4>3. 考试规则</h4>
        <p>用户需遵守考试规则，不得作弊或使用不正当手段。</p>
        
        <h4>4. 其他条款</h4>
        <p>其他未尽事宜，以平台最终解释为准。</p>
      </div>
    </el-dialog>

    <!-- 隐私政策对话框 -->
    <el-dialog v-model="showPrivacy" title="隐私政策" width="60%">
      <div class="privacy-content">
        <h4>1. 信息收集</h4>
        <p>我们仅收集必要的用户信息用于提供服务。</p>
        
        <h4>2. 信息使用</h4>
        <p>用户信息仅用于考试服务，不会泄露给第三方。</p>
        
        <h4>3. 信息保护</h4>
        <p>我们采用安全措施保护用户信息。</p>
        
        <h4>4. 其他条款</h4>
        <p>其他未尽事宜，以平台最终解释为准。</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { CreditCard, Wallet, Phone, User } from '@element-plus/icons-vue'
import { formatDuration } from '@/utils/format'

export default {
  name: 'ExamPurchase',
  components: {
    CreditCard,
    Wallet,
    Phone,
    User
  },
  props: {
    exam: {
      type: Object,
      required: true
    },
    subject: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['success', 'cancel'],
  setup(props, { emit }) {
    // 响应式数据
    const purchasing = ref(false)
    const validatingCoupon = ref(false)
    const couponCode = ref('')
    const validatedCoupon = ref(null)
    const selectedPaymentMethod = ref('alipay')
    const agreedToTerms = ref(false)
    const showTerms = ref(false)
    const showPrivacy = ref(false)
    
    // 支付方式
    const paymentMethods = reactive([
      {
        value: 'alipay',
        name: '支付宝',
        description: '支持花呗分期',
        icon: 'CreditCard'
      },
      {
        value: 'wechat',
        name: '微信支付',
        description: '安全便捷',
        icon: 'Wallet'
      },
      {
        value: 'paypal',
        name: 'PayPal',
        description: '国际支付',
        icon: 'CreditCard'
      },
      {
        value: 'admin',
        name: '联系管理员',
        description: '线下支付',
        icon: 'User'
      }
    ])
    
    // 计算属性
    const examPrice = computed(() => {
      return props.subject.price || 0
    })
    
    const originalPrice = computed(() => {
      return props.subject.original_price || props.subject.price || 0
    })
    
    const discountRate = computed(() => {
      if (originalPrice.value <= 0) return 100
      return Math.round((examPrice.value / originalPrice.value) * 100)
    })
    
    const couponDiscount = computed(() => {
      if (!validatedCoupon.value) return 0
      
      if (validatedCoupon.value.type === 'percentage') {
        return Math.round(examPrice.value * (validatedCoupon.value.value / 100))
      } else {
        return Math.min(validatedCoupon.value.value, examPrice.value)
      }
    })
    
    const finalPrice = computed(() => {
      return Math.max(0, examPrice.value - couponDiscount.value)
    })
    
    // 方法
    const selectPaymentMethod = (method) => {
      selectedPaymentMethod.value = method
    }
    
    const validateCoupon = async () => {
      if (!couponCode.value.trim()) {
        ElMessage.warning('请输入优惠券代码')
        return
      }
      
      try {
        validatingCoupon.value = true
        
        // TODO: 实现优惠券验证API
        // const response = await couponApi.validateCoupon({
        //   code: couponCode.value,
        //   exam_id: props.exam.id
        // })
        
        // 模拟验证结果
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 模拟优惠券数据
        validatedCoupon.value = {
          id: 1,
          name: '新用户优惠券',
          type: 'fixed',
          value: 10,
          min_amount: 0
        }
        
        ElMessage.success('优惠券验证成功')
      } catch (error) {
        ElMessage.error('优惠券验证失败')
        validatedCoupon.value = null
        console.error('Validate coupon error:', error)
      } finally {
        validatingCoupon.value = false
      }
    }
    
    const handlePurchase = async () => {
      if (!agreedToTerms.value) {
        ElMessage.warning('请先同意用户协议')
        return
      }
      
      if (finalPrice.value <= 0) {
        ElMessage.warning('应付金额不能为0')
        return
      }
      
      try {
        purchasing.value = true
        
        // 创建订单
        const orderData = {
          exam_id: props.exam.id,
          payment_method: selectedPaymentMethod.value,
          amount: finalPrice.value,
          coupon_id: validatedCoupon.value?.id,
          coupon_code: couponCode.value
        }
        
        // TODO: 实现创建订单API
        // const response = await orderApi.createOrder(orderData)
        
        // 模拟创建订单
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        if (selectedPaymentMethod.value === 'admin') {
          // 联系管理员支付
          ElMessage.success('订单已创建，请联系管理员完成支付')
          emit('success')
        } else {
          // 跳转到支付页面
          ElMessage.success('订单创建成功，正在跳转到支付页面')
          // TODO: 跳转到支付页面
          emit('success')
        }
      } catch (error) {
        ElMessage.error('购买失败')
        console.error('Purchase error:', error)
      } finally {
        purchasing.value = false
      }
    }
    
    const handleCancel = () => {
      emit('cancel')
    }
    
    return {
      purchasing,
      validatingCoupon,
      couponCode,
      validatedCoupon,
      selectedPaymentMethod,
      agreedToTerms,
      showTerms,
      showPrivacy,
      paymentMethods,
      examPrice,
      originalPrice,
      discountRate,
      couponDiscount,
      finalPrice,
      selectPaymentMethod,
      validateCoupon,
      handlePurchase,
      handleCancel,
      formatDuration
    }
  }
}
</script>

<style scoped>
.exam-purchase {
  padding: 20px;
}

.purchase-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.purchase-header h3 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.exam-info {
  color: #909399;
  font-size: 14px;
}

.purchase-content {
  margin-bottom: 30px;
}

.price-section {
  margin-bottom: 25px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.price-display {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 10px;
}

.price-current {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-label {
  color: #606266;
  font-size: 16px;
}

.price-value {
  color: #e6a23c;
  font-size: 24px;
  font-weight: 600;
}

.price-original {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-original .price-value {
  color: #909399;
  font-size: 16px;
  text-decoration: line-through;
}

.discount-info {
  display: flex;
  justify-content: flex-end;
}

.coupon-section,
.payment-section,
.order-summary {
  margin-bottom: 25px;
}

.section-title {
  margin-bottom: 15px;
}

.section-title h4 {
  margin: 0;
  color: #303133;
  font-size: 16px;
  font-weight: 500;
}

.coupon-input {
  margin-bottom: 10px;
}

.coupon-info {
  display: flex;
  justify-content: center;
}

.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.payment-method {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.payment-method:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.method-selected {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.method-icon {
  margin-right: 15px;
  color: #409eff;
}

.method-info {
  flex: 1;
}

.method-name {
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.method-desc {
  font-size: 12px;
  color: #909399;
}

.method-radio {
  margin-left: 10px;
}

.summary-items {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.summary-item.total {
  padding-top: 10px;
  border-top: 1px solid #e4e7ed;
  font-weight: 600;
  font-size: 16px;
}

.item-label {
  color: #606266;
}

.item-value {
  color: #303133;
}

.item-value.discount {
  color: #67c23a;
}

.agreement-section {
  margin-bottom: 20px;
  text-align: center;
}

.purchase-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-top: 1px solid #ebeef5;
}

.footer-info {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  color: #606266;
}

.final-price {
  color: #e6a23c;
  font-size: 20px;
  font-weight: 600;
}

.footer-actions {
  display: flex;
  gap: 10px;
}

.terms-content,
.privacy-content {
  line-height: 1.6;
}

.terms-content h4,
.privacy-content h4 {
  margin: 20px 0 10px 0;
  color: #303133;
  font-size: 16px;
}

.terms-content p,
.privacy-content p {
  margin: 0 0 15px 0;
  color: #606266;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .exam-purchase {
    padding: 15px;
  }
  
  .price-display {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .purchase-footer {
    flex-direction: column;
    gap: 15px;
  }
  
  .footer-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>
