<template>
  <el-card v-loading="loading" class="page-card form-card">
    <template #header>
      <span>{{ isCreate ? '新建健康记录' : '编辑健康记录' }}</span>
    </template>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="max-width:500px">
      <el-form-item label="居民" prop="resident_id" v-if="isCreate">
        <el-select v-model="form.resident_id" placeholder="请选择居民" filterable style="width:100%">
          <el-option v-for="r in residents" :key="r.id" :label="`${r.name} (ID:${r.id})`" :value="r.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="体检时间" prop="checkup_date">
        <el-date-picker v-model="form.checkup_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width:100%" />
      </el-form-item>
      <el-form-item label="身高(cm)" prop="height">
        <el-input-number v-model="form.height" :min="0" :precision="1" style="width:100%" />
      </el-form-item>
      <el-form-item label="体重(kg)" prop="weight">
        <el-input-number v-model="form.weight" :min="0" :precision="1" style="width:100%" />
      </el-form-item>
      <el-form-item label="疾病" prop="diseases">
        <el-input v-model="form.diseases" type="textarea" placeholder="多个疾病用逗号分隔" />
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
import { getHealthById, createHealth, updateHealth } from '@/api/health'
import { getResidents } from '@/api/resident'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const id = computed(() => route.params.id)
const isCreate = computed(() => route.path.includes('/health/create'))
const formRef = ref(null)
const loading = ref(false)
const residents = ref([])
const form = reactive({
  resident_id: null,
  checkup_date: '',
  height: null,
  weight: null,
  diseases: ''
})
const rules = computed(() => {
  const r = {
    checkup_date: [{ required: true, message: '请选择体检时间', trigger: 'change' }],
    height: [{ required: true, message: '请输入身高', trigger: 'blur' }],
    weight: [{ required: true, message: '请输入体重', trigger: 'blur' }]
  }
  if (isCreate.value) r.resident_id = [{ required: true, message: '请选择居民', trigger: 'change' }]
  return r
})

async function fetchResidents() {
  const res = await getResidents({ page: 1, limit: 1000 })
  residents.value = Array.isArray(res) ? res : []
}

async function fetch() {
  if (isCreate.value) return
  loading.value = true
  try {
    const res = await getHealthById(id.value)
    Object.assign(form, { checkup_date: res.checkup_date, height: res.height, weight: res.weight, diseases: res.diseases || '' })
  } finally {
    loading.value = false
  }
}

async function onSubmit() {
  await formRef.value?.validate()
  loading.value = true
  try {
    if (isCreate.value) {
      await createHealth({
        resident_id: form.resident_id,
        checkup_date: form.checkup_date,
        height: form.height,
        weight: form.weight,
        diseases: form.diseases || ''
      })
      ElMessage.success('创建成功')
    } else {
      await updateHealth(id.value, {
        checkup_date: form.checkup_date,
        height: form.height,
        weight: form.weight,
        diseases: form.diseases || ''
      })
      ElMessage.success('保存成功')
    }
    router.push('/health')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (isCreate.value) await fetchResidents()
  else await fetch()
})
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
