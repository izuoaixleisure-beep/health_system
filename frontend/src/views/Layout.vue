<template>
  <el-container class="layout">
    <el-aside width="200px" class="aside">
      <div class="logo">健康档案</div>
      <el-menu :default-active="$route.path" router>
        <el-menu-item index="/">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/residents">
          <el-icon><User /></el-icon>
          <span>居民信息</span>
        </el-menu-item>
        <el-menu-item index="/health">
          <el-icon><Document /></el-icon>
          <span>健康档案</span>
        </el-menu-item>
        <template v-if="authStore.isDoctor">
          <el-menu-item index="/health/create">
            <el-icon><Plus /></el-icon>
            <span>新建健康记录</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>{{ authStore.user?.role === 'doctor' ? '医生' : '居民' }}：{{ authStore.user?.username }}</span>
        <el-button type="danger" link @click="logout">退出</el-button>
      </el-header>
      <el-main class="main">
        <router-view v-slot="{ Component }">
          <keep-alive :include="[]">
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { House, User, Document, Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.clearUser()
  router.push('/login')
}
</script>

<style scoped>
.layout { height: 100vh; }
.aside {
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.15);
}
.logo {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  padding: 24px;
  text-align: center;
  letter-spacing: 2px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
:deep(.el-menu) {
  border-right: none;
  background: transparent;
  padding: 12px 0;
}
:deep(.el-menu-item) {
  color: #bdc3c7;
  margin: 4px 12px;
  border-radius: 8px;
  transition: all 0.25s ease;
}
:deep(.el-menu-item:hover) {
  background: rgba(64, 158, 255, 0.15);
  color: #409eff;
}
:deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(64, 158, 255, 0.3) 0%, rgba(64, 158, 255, 0.1) 100%);
  color: #409eff;
  border-left: 3px solid #409eff;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 0 24px;
  font-size: 15px;
  color: #303133;
}
.main {
  background: linear-gradient(180deg, #f5f7fa 0%, #e8ecf1 100%);
  padding: 24px;
  overflow-y: auto;
}
.main :deep(.el-card) {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
</style>
