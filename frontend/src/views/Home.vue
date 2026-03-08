<template>
  <el-card class="home-card">
    <template #header>
      <div class="header-inner">
        <el-icon class="welcome-icon"><House /></el-icon>
        <span>欢迎使用居民健康档案系统</span>
      </div>
    </template>
    <div class="welcome-content">
      <p class="role-tip">
        您已登录为 <el-tag :type="authStore.isDoctor ? 'success' : 'info'" size="large">{{ authStore.isDoctor ? '医生' : '居民' }}</el-tag>，请从左侧菜单选择功能。
      </p>
      <el-divider />
      <p v-if="authStore.isResident" class="desc">
        <el-icon><User /></el-icon>
        居民可查看自己的居民信息、查看自己的健康档案。
      </p>
      <p v-else class="desc">
        <el-icon><Monitor /></el-icon>
        医生可管理所有居民信息、创建和编辑健康档案。
      </p>
    </div>
  </el-card>
</template>

<script setup>
import { House, User, Monitor } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.home-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  padding: 24px;
}
.header-inner {
  display: flex;
  align-items: center;
  gap: 12px;
}
.welcome-icon {
  font-size: 28px;
}
.welcome-content {
  padding: 8px 0;
  line-height: 1.8;
}
.role-tip {
  font-size: 16px;
  color: #303133;
}
.desc {
  font-size: 15px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 8px;
}
.desc .el-icon {
  color: #409eff;
  font-size: 20px;
}
</style>
