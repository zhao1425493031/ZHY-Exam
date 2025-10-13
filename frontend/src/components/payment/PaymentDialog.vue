<template>
  <el-dialog
    v-model="visible"
    title="选择支付方式"
    width="500px"
    :before-close="handleClose"
    center
  >
    <div class="payment-dialog">
      <!-- 课程信息 -->
      <div class="course-info">
        <h3>{{ courseInfo.name }}</h3>
        <p class="course-price">¥{{ courseInfo.price }}</p>
      </div>
      
      <!-- 支付方式选择步骤 -->
      <div v-if="currentStep === 'select'" class="payment-methods">
        <h4>请选择支付方式</h4>
        <div class="payment-options">
          <!-- 支付宝 -->
          <div 
            class="payment-option"
            :class="{ active: selectedMethod === 'alipay' }"
            @click="selectPaymentMethod('alipay')"
          >
            <div class="payment-icon alipay">
              <svg viewBox="0 0 1024 1024" width="32" height="32">
                <path fill="#1677FF" d="M789.061 279.64c-1.664-10.368-5.632-19.456-11.52-27.136-5.888-7.68-13.312-13.824-22.016-18.432-8.704-4.608-18.432-7.68-28.672-9.216-10.24-1.536-20.992-1.536-31.744 0-10.752 1.536-20.992 4.608-30.72 9.216-9.728 4.608-17.664 10.752-23.552 18.432-5.888 7.68-9.856 16.768-11.52 27.136-1.664 10.368-1.664 20.992 0 31.36 1.664 10.368 5.632 19.456 11.52 27.136 5.888 7.68 13.312 13.824 22.016 18.432 8.704 4.608 18.432 7.68 28.672 9.216 10.24 1.536 20.992 1.536 31.744 0 10.752-1.536 20.992-4.608 30.72-9.216 9.728-4.608 17.664-10.752 23.552-18.432 5.888-7.68 9.856-16.768 11.52-27.136 1.664-10.368 1.664-20.992 0-31.36z"/>
                <path fill="#1677FF" d="M512 64C264.576 64 64 264.576 64 512s200.576 448 448 448 448-200.576 448-448S759.424 64 512 64zm0 832c-212.096 0-384-171.904-384-384S299.904 128 512 128s384 171.904 384 384-171.904 384-384 384z"/>
              </svg>
            </div>
            <div class="payment-info">
              <h5>支付宝</h5>
              <p>使用支付宝扫码支付</p>
            </div>
            <div class="payment-radio">
              <el-radio v-model="selectedMethod" label="alipay" />
            </div>
          </div>
          
          <!-- 微信支付 -->
          <div 
            class="payment-option"
            :class="{ active: selectedMethod === 'wechat' }"
            @click="selectPaymentMethod('wechat')"
          >
            <div class="payment-icon wechat">
              <svg viewBox="0 0 1024 1024" width="32" height="32">
                <path fill="#07C160" d="M512 64C264.576 64 64 264.576 64 512s200.576 448 448 448 448-200.576 448-448S759.424 64 512 64zm0 832c-212.096 0-384-171.904-384-384S299.904 128 512 128s384 171.904 384 384-171.904 384-384 384z"/>
                <path fill="#07C160" d="M512 256c-141.312 0-256 114.688-256 256s114.688 256 256 256 256-114.688 256-256-114.688-256-256-256zm0 448c-106.048 0-192-85.952-192-192s85.952-192 192-192 192 85.952 192 192-85.952 192-192 192z"/>
              </svg>
            </div>
            <div class="payment-info">
              <h5>微信支付</h5>
              <p>使用微信扫码支付</p>
            </div>
            <div class="payment-radio">
              <el-radio v-model="selectedMethod" label="wechat" />
            </div>
          </div>
          
          <!-- PayPal -->
          <div 
            class="payment-option"
            :class="{ active: selectedMethod === 'paypal' }"
            @click="selectPaymentMethod('paypal')"
          >
            <div class="payment-icon paypal">
              <svg viewBox="0 0 1024 1024" width="32" height="32">
                <path fill="#0070BA" d="M512 64C264.576 64 64 264.576 64 512s200.576 448 448 448 448-200.576 448-448S759.424 64 512 64zm0 832c-212.096 0-384-171.904-384-384S299.904 128 512 128s384 171.904 384 384-171.904 384-384 384z"/>
                <path fill="#0070BA" d="M512 256c-141.312 0-256 114.688-256 256s114.688 256 256 256 256-114.688 256-256-114.688-256-256-256zm0 448c-106.048 0-192-85.952-192-192s85.952-192 192-192 192 85.952 192 192-85.952 192-192 192z"/>
              </svg>
            </div>
            <div class="payment-info">
              <h5>PayPal</h5>
              <p>使用PayPal账户支付</p>
            </div>
            <div class="payment-radio">
              <el-radio v-model="selectedMethod" label="paypal" />
            </div>
          </div>
          
          <!-- 联系管理员 -->
          <div 
            class="payment-option"
            :class="{ active: selectedMethod === 'admin' }"
            @click="selectPaymentMethod('admin')"
          >
            <div class="payment-icon admin">
              <el-icon size="32"><User /></el-icon>
            </div>
            <div class="payment-info">
              <h5>联系管理员</h5>
              <p>通过客服完成支付</p>
            </div>
            <div class="payment-radio">
              <el-radio v-model="selectedMethod" label="admin" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- 二维码支付步骤 -->
      <div v-if="currentStep === 'qr'" class="qr-payment-step">
        <div class="qr-header">
          <h4>{{ qrCodeData.method === 'alipay' ? '支付宝扫码支付' : '微信扫码支付' }}</h4>
          <p>请使用{{ qrCodeData.method === 'alipay' ? '支付宝' : '微信' }}扫描下方二维码完成支付</p>
        </div>
        
        <div class="qr-code-container">
          <div class="qr-code-wrapper">
            <img 
              :src="qrCodeData.qr_code_url" 
              :alt="qrCodeData.method === 'alipay' ? '支付宝收款码' : '微信收款码'"
              class="qr-code-image"
            />
            <div class="qr-loading" v-if="!qrCodeData.qr_code_url">
              <el-icon class="is-loading"><Loading /></el-icon>
              <p>正在生成收款码...</p>
            </div>
          </div>
          
          <div class="qr-info">
            <div class="amount-info">
              <span class="amount-label">支付金额</span>
              <span class="amount-value">¥{{ qrCodeData.amount }}</span>
            </div>
            <div class="order-info">
              <span class="order-label">订单号</span>
              <span class="order-value">{{ qrCodeData.order_id }}</span>
            </div>
          </div>
        </div>
        
        <div class="qr-tips">
          <el-alert
            :title="qrCodeData.method === 'alipay' ? '支付宝支付提示' : '微信支付提示'"
            type="info"
            :closable="false"
            show-icon
          >
            <template #default>
              <ul>
                <li>请使用{{ qrCodeData.method === 'alipay' ? '支付宝' : '微信' }}扫描上方二维码</li>
                <li>确认支付金额后完成付款</li>
                <li>支付成功后请点击"支付完成"按钮</li>
                <li>如遇问题请联系客服</li>
              </ul>
            </template>
          </el-alert>
        </div>
      </div>
      
      <!-- 支付说明 -->
      <div v-if="currentStep === 'select'" class="payment-notice">
        <el-alert
          title="支付说明"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            <ul>
              <li>支付成功后，课程将自动添加到您的账户</li>
              <li>如遇支付问题，请联系客服处理</li>
              <li>支持7天无理由退款</li>
            </ul>
          </template>
        </el-alert>
      </div>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button v-if="currentStep === 'select'" @click="handleClose">取消</el-button>
        <el-button v-if="currentStep === 'qr'" @click="goBack">返回</el-button>
        
        <el-button 
          v-if="currentStep === 'select'"
          type="primary" 
          @click="handlePayment"
          :loading="paying"
          :disabled="!selectedMethod"
        >
          确认支付
        </el-button>
        
        <el-button 
          v-if="currentStep === 'qr'"
          type="success" 
          @click="handlePaymentComplete"
        >
          支付完成
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Loading } from '@element-plus/icons-vue'
import { paymentApi } from '@/api/payment'

export default {
  name: 'PaymentDialog',
  components: {
    User,
    Loading
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    courseInfo: {
      type: Object,
      required: true
    }
  },
  emits: ['update:modelValue', 'payment-success', 'payment-cancel'],
  setup(props, { emit }) {
    const visible = ref(false)
    const selectedMethod = ref('')
    const paying = ref(false)
    const showQRCode = ref(false)
    const qrCodeData = ref(null)
    const currentStep = ref('select') // select, qr, success
    
    // 监听modelValue变化
    watch(() => props.modelValue, (newVal) => {
      visible.value = newVal
      if (newVal) {
        selectedMethod.value = ''
        showQRCode.value = false
        qrCodeData.value = null
        currentStep.value = 'select'
      }
    })
    
    // 监听visible变化
    watch(visible, (newVal) => {
      emit('update:modelValue', newVal)
    })
    
    // 选择支付方式
    const selectPaymentMethod = (method) => {
      selectedMethod.value = method
    }
    
    // 关闭弹窗
    const handleClose = () => {
      visible.value = false
      emit('payment-cancel')
    }
    
    // 返回上一步
    const goBack = () => {
      currentStep.value = 'select'
      showQRCode.value = false
      qrCodeData.value = null
    }
    
    // 支付完成
    const handlePaymentComplete = () => {
      ElMessage.success('支付成功！')
      visible.value = false
      emit('payment-success', {
        method: qrCodeData.value.method,
        courseId: props.courseInfo.id,
        orderId: qrCodeData.value.order_id
      })
    }
    
    // 处理支付
    const handlePayment = async () => {
      if (!selectedMethod.value) {
        ElMessage.warning('请选择支付方式')
        return
      }
      
      paying.value = true
      
      try {
        switch (selectedMethod.value) {
          case 'alipay':
            await handleAlipayPayment()
            break
          case 'wechat':
            await handleWechatPayment()
            break
          case 'paypal':
            await handlePaypalPayment()
            break
          case 'admin':
            await handleAdminPayment()
            break
        }
      } catch (error) {
        console.error('支付失败:', error)
        ElMessage.error('支付失败，请重试')
      } finally {
        paying.value = false
      }
    }
    
    // 支付宝支付
    const handleAlipayPayment = async () => {
      try {
        ElMessage.info('正在生成支付宝收款码...')
        
        const response = await paymentApi.alipayPayment({
          course_id: props.courseInfo.id,
          amount: props.courseInfo.price
        })
        
        if (response.code === 200) {
          // 显示支付宝收款二维码
          qrCodeData.value = {
            method: 'alipay',
            order_id: response.data.order_id,
            amount: response.data.amount,
            qr_code_url: response.data.qr_code_url,
            subject_name: response.data.subject_name
          }
          currentStep.value = 'qr'
          showQRCode.value = true
        } else {
          ElMessage.error(response.message || '生成收款码失败')
        }
      } catch (error) {
        console.error('支付宝支付失败:', error)
        ElMessage.error('生成收款码失败，请重试')
      }
    }
    
    // 微信支付
    const handleWechatPayment = async () => {
      try {
        ElMessage.info('正在生成微信收款码...')
        
        const response = await paymentApi.wechatPayment({
          course_id: props.courseInfo.id,
          amount: props.courseInfo.price
        })
        
        if (response.code === 200) {
          // 显示微信收款二维码
          qrCodeData.value = {
            method: 'wechat',
            order_id: response.data.order_id,
            amount: response.data.amount,
            qr_code_url: response.data.qr_code_url,
            subject_name: response.data.subject_name
          }
          currentStep.value = 'qr'
          showQRCode.value = true
        } else {
          ElMessage.error(response.message || '生成收款码失败')
        }
      } catch (error) {
        console.error('微信支付失败:', error)
        ElMessage.error('生成收款码失败，请重试')
      }
    }
    
    // PayPal支付
    const handlePaypalPayment = async () => {
      try {
        ElMessage.info('正在跳转到PayPal支付...')
        
        const response = await paymentApi.paypalPayment({
          course_id: props.courseInfo.id,
          amount: props.courseInfo.price
        })
        
        if (response.code === 200) {
          // 跳转到PayPal支付页面
          window.open(response.data.payment_url, '_blank')
          
          // 模拟支付成功（实际应该通过回调或轮询确认）
          setTimeout(() => {
            ElMessage.success('支付成功！')
            visible.value = false
            emit('payment-success', {
              method: 'paypal',
              courseId: props.courseInfo.id,
              orderId: response.data.order_id
            })
          }, 3000)
        } else {
          ElMessage.error(response.message || '创建支付订单失败')
        }
      } catch (error) {
        console.error('PayPal支付失败:', error)
        ElMessage.error('支付失败，请重试')
      }
    }
    
    // 联系管理员支付
    const handleAdminPayment = async () => {
      try {
        ElMessage.info('正在提交支付申请...')
        
        const response = await paymentApi.adminPayment({
          course_id: props.courseInfo.id,
          amount: props.courseInfo.price
        })
        
        if (response.code === 200) {
          ElMessage.success('已提交支付申请，管理员将在24小时内处理')
          visible.value = false
          emit('payment-success', {
            method: 'admin',
            courseId: props.courseInfo.id,
            orderId: response.data.order_id
          })
        } else {
          ElMessage.error(response.message || '提交支付申请失败')
        }
      } catch (error) {
        console.error('联系管理员支付失败:', error)
        ElMessage.error('提交失败，请重试')
      }
    }
    
    return {
      visible,
      selectedMethod,
      paying,
      showQRCode,
      qrCodeData,
      currentStep,
      selectPaymentMethod,
      handleClose,
      handlePayment,
      goBack,
      handlePaymentComplete
    }
  }
}
</script>

<style lang="scss" scoped>
.payment-dialog {
  .course-info {
    text-align: center;
    margin-bottom: 2rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    
    h3 {
      margin: 0 0 0.5rem 0;
      color: #333;
    }
    
    .course-price {
      font-size: 1.5rem;
      font-weight: bold;
      color: #e74c3c;
      margin: 0;
    }
  }
  
  .payment-methods {
    margin-bottom: 2rem;
    
    h4 {
      margin-bottom: 1rem;
      color: #333;
    }
    
    .payment-options {
      .payment-option {
        display: flex;
        align-items: center;
        padding: 1rem;
        border: 2px solid #e6e6e6;
        border-radius: 8px;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        
        &:hover {
          border-color: #409eff;
          background: #f0f9ff;
        }
        
        &.active {
          border-color: #409eff;
          background: #f0f9ff;
        }
        
        .payment-icon {
          width: 48px;
          height: 48px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 8px;
          margin-right: 1rem;
          
          &.alipay {
            background: #1677ff;
            color: white;
          }
          
          &.wechat {
            background: #07c160;
            color: white;
          }
          
          &.paypal {
            background: #0070ba;
            color: white;
          }
          
          &.admin {
            background: #909399;
            color: white;
          }
        }
        
        .payment-info {
          flex: 1;
          
          h5 {
            margin: 0 0 0.25rem 0;
            color: #333;
          }
          
          p {
            margin: 0;
            color: #666;
            font-size: 0.9rem;
          }
        }
        
        .payment-radio {
          margin-left: 1rem;
        }
      }
    }
  }
  
  .payment-notice {
    margin-bottom: 1rem;
    
    ul {
      margin: 0.5rem 0 0 0;
      padding-left: 1.2rem;
      
      li {
        margin-bottom: 0.25rem;
        color: #666;
        font-size: 0.9rem;
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 二维码支付步骤样式 */
.qr-payment-step {
  .qr-header {
    text-align: center;
    margin-bottom: 2rem;
    
    h4 {
      margin: 0 0 0.5rem 0;
      color: #333;
      font-size: 1.2rem;
    }
    
    p {
      margin: 0;
      color: #666;
      font-size: 0.9rem;
    }
  }
  
  .qr-code-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
    
    .qr-code-wrapper {
      position: relative;
      width: 200px;
      height: 200px;
      border: 2px solid #e6e6e6;
      border-radius: 12px;
      overflow: hidden;
      background: #fff;
      
      .qr-code-image {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
      
      .qr-loading {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: #666;
        
        .el-icon {
          font-size: 2rem;
          margin-bottom: 0.5rem;
        }
        
        p {
          margin: 0;
          font-size: 0.9rem;
        }
      }
    }
    
    .qr-info {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      width: 100%;
      
      .amount-info,
      .order-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 8px;
        
        .amount-label,
        .order-label {
          color: #666;
          font-size: 0.9rem;
        }
        
        .amount-value {
          color: #e74c3c;
          font-weight: bold;
          font-size: 1.1rem;
        }
        
        .order-value {
          color: #333;
          font-family: monospace;
          font-size: 0.8rem;
        }
      }
    }
  }
  
  .qr-tips {
    ul {
      margin: 0.5rem 0 0 0;
      padding-left: 1.2rem;
      
      li {
        margin-bottom: 0.25rem;
        color: #666;
        font-size: 0.9rem;
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .qr-payment-step {
    .qr-code-container {
      .qr-code-wrapper {
        width: 160px;
        height: 160px;
      }
      
      .qr-info {
        .amount-info,
        .order-info {
          padding: 0.5rem;
          
          .order-value {
            font-size: 0.7rem;
          }
        }
      }
    }
  }
}
</style>
