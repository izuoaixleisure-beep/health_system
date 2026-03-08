<template>
  <el-card class="page-card">
    <template #header>
      <span>居民信息</span>
    </template>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别" width="80" />
      <el-table-column prop="birth_date" label="出生日期" width="120" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="address" label="地址" min-width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="200" fixed="right" v-if="authStore.isDoctor">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/residents/${row.id}`)">详情</el-button>
          <el-button link type="primary" @click="$router.push(`/residents/${row.id}/edit`)">编辑</el-button>
          <el-popconfirm title="确定删除该居民？将同时删除其用户和健康记录" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button link type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-if="authStore.isDoctor"
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
import { getResidents, deleteResident } from '@/api/resident'
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
    const res = await getResidents({ page: page.value, limit: limit.value })
    list.value = Array.isArray(res) ? res : []
    total.value = list.value.length
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  try {
    await deleteResident(id)
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
