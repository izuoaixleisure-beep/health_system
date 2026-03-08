<template>
  <el-card class="page-card">
    <template #header>
      <span>健康档案</span>
    </template>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="resident_id" label="居民ID" width="90" />
      <el-table-column prop="checkup_date" label="体检时间" width="120" />
      <el-table-column prop="height" label="身高(cm)" width="100" />
      <el-table-column prop="weight" label="体重(kg)" width="100" />
      <el-table-column prop="diseases" label="疾病" min-width="120" show-overflow-tooltip />
      <el-table-column label="操作" width="180" fixed="right" v-if="authStore.isDoctor">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/health/${row.id}/edit`)">编辑</el-button>
          <el-popconfirm title="确定删除该健康记录？" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button link type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      v-model:page-size="limit"
      :page-sizes="[10, 20, 50]"
      layout="total, sizes, prev, pager, next"
      :total="total"
      @current-change="fetch"
      @size-change="fetch"
      style="margin-top: 16px; justify-content: flex-end;"
    />
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHealthList, deleteHealth } from '@/api/health'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const list = ref([])
const loading = ref(false)
const page = ref(1)
const limit = ref(10)
const total = ref(0)

async function fetch() {
  loading.value = true
  try {
    const res = await getHealthList({ page: page.value, limit: limit.value })
    list.value = Array.isArray(res) ? res : []
    total.value = list.value.length
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  try {
    await deleteHealth(id)
    ElMessage.success('删除成功')
    await fetch()
  } catch (_) {}
}

onMounted(() => { fetch() })
</script>

<style scoped>
.page-card :deep(.el-card__header) {
  font-size: 17px;
  font-weight: 600;
  color: #303133;
  padding: 18px 24px;
  border-bottom: 1px solid #ebeef5;
}
.page-card :deep(.el-card__body) {
  padding: 24px;
}
.page-card :deep(.el-table) {
  font-size: 14px;
}
.page-card :deep(.el-table th) {
  background: #fafafa;
  color: #606266;
  font-weight: 600;
}
.page-card :deep(.el-pagination) {
  display: flex;
}
</style>
