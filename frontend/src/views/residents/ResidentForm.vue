<template>
  <el-card v-loading="loading" class="page-card form-card">
    <template #header>
      <span>{{ isEdit ? '编辑居民' : '新建居民' }}</span>
    </template>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="max-width:500px">
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
      <el-form-item>
        <el-button type="primary" @click="onSubmit">保存</el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getResidentById, updateResident } from '@/api/resident'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const id = computed(() => route.params.id)
const isEdit = computed(() => !!id.value && id.value !== 'create')
const formRef = ref(null)
const loading = ref(false)
const form = reactive({ name: '', gender: '', birth_date: '', phone: '', address: '' })
const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  birth_date: [{ required: true, message: '请选择出生日期', trigger: 'change' }],
  phone: [{ required: true, message: '请输入电话', trigger: 'blur' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }]
}

async function fetch() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const res = await getResidentById(id.value)
    Object.assign(form, res)
  } finally {
    loading.value = false
  }
}

async function onSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    await updateResident(id.value, form)
    ElMessage.success('保存成功')
    router.push('/residents')
  } finally {
    loading.value = false
  }
}

onMounted(() => { fetch() })
</script>

<style scoped>
.page-card :deep(.el-card__header) {
  font-size: 17px;
  font-weight: 600;
  padding: 18px 24px;
  border-bottom: 1px solid #ebeef5;
}
.page-card :deep(.el-card__body) {
  padding: 28px 24px;
}
.form-card :deep(.el-input__wrapper),
.form-card :deep(.el-textarea__inner) {
  border-radius: 8px;
}
</style>
