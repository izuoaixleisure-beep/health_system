<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <span>居民健康档案系统 - 注册</span>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" @submit.prevent="onSubmit">
        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="form.role">
            <el-radio value="doctor">医生</el-radio>
            <el-radio value="resident">居民</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <template v-if="form.role === 'resident'">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="form.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="form.gender">
              <el-radio value="男">男</el-radio>
              <el-radio value="女">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="出生日期" prop="birth_date">
            <el-date-picker v-model="form.birth_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width:100%" />
          </el-form-item>
          <el-form-item label="电话" prop="phone">
            <el-input v-model="form.phone" placeholder="请输入电话" />
          </el-form-item>
          <el-form-item label="地址" prop="address">
            <el-input v-model="form.address" type="textarea" placeholder="请输入地址" />
          </el-form-item>
        </template>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="onSubmit" style="width:100%">注册</el-button>
        </el-form-item>
        <el-form-item>
          <el-button text type="primary" @click="$router.push('/login')">已有账号？去登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const form = reactive({
  role: 'resident',
  username: '',
  password: '',
  name: '',
  gender: '',
  birth_date: '',
  phone: '',
  address: ''
})

const rules = computed(() => {
  const base = {
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
  }
  if (form.role === 'resident') {
    base.name = [{ required: true, message: '请输入姓名', trigger: 'blur' }]
    base.gender = [{ required: true, message: '请选择性别', trigger: 'change' }]
    base.birth_date = [{ required: true, message: '请选择出生日期', trigger: 'change' }]
    base.phone = [{ required: true, message: '请输入电话', trigger: 'blur' }]
    base.address = [{ required: true, message: '请输入地址', trigger: 'blur' }]
  }
  return base
})

async function onSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const data = { ...form }
    if (form.role === 'doctor') {
      delete data.name
      delete data.gender
      delete data.birth_date
      delete data.phone
      delete data.address
    }
    await register(data)
    ElMessage.success('注册成功')
    router.push('/login')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e8ba3 100%);
  padding: 24px 0;
}
.register-card {
  width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.5s ease-out;
}
.register-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  padding: 20px;
}
.register-card :deep(.el-card__body) {
  padding: 28px;
}
.register-card :deep(.el-input__wrapper),
.register-card :deep(.el-textarea__inner) {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.register-card :deep(.el-button--primary) {
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
