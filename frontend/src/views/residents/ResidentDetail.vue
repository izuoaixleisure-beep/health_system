<template>
  <el-card v-loading="loading" class="page-card">
    <template #header>
      <span>居民详情</span>
      <el-button type="primary" link style="float:right" @click="$router.push(`/residents/${id}/edit`)">编辑</el-button>
    </template>
    <el-descriptions :column="1" border v-if="data">
      <el-descriptions-item label="ID">{{ data.id }}</el-descriptions-item>
      <el-descriptions-item label="姓名">{{ data.name }}</el-descriptions-item>
      <el-descriptions-item label="性别">{{ data.gender }}</el-descriptions-item>
      <el-descriptions-item label="出生日期">{{ data.birth_date }}</el-descriptions-item>
      <el-descriptions-item label="电话">{{ data.phone }}</el-descriptions-item>
      <el-descriptions-item label="地址">{{ data.address }}</el-descriptions-item>
    </el-descriptions>
    <el-button style="margin-top:16px" @click="$router.back()">返回</el-button>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getResidentById } from '@/api/resident'

const route = useRoute()
const id = computed(() => route.params.id)
const data = ref(null)
const loading = ref(false)

async function fetch() {
  loading.value = true
  try {
    data.value = await getResidentById(id.value)
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
  padding: 24px;
}
.page-card :deep(.el-descriptions__label) {
  font-weight: 500;
  color: #606266;
  width: 120px;
}
</style>
