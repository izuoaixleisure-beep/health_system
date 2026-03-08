import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue'), meta: { guest: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/Register.vue'), meta: { guest: true } },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Home', component: () => import('@/views/Home.vue') },
      { path: 'residents', name: 'ResidentList', component: () => import('@/views/residents/ResidentList.vue') },
      { path: 'residents/:id', name: 'ResidentDetail', component: () => import('@/views/residents/ResidentDetail.vue'), meta: { doctorOnly: true } },
      { path: 'residents/:id/edit', name: 'ResidentEdit', component: () => import('@/views/residents/ResidentForm.vue'), meta: { doctorOnly: true } },
      { path: 'health', name: 'HealthList', component: () => import('@/views/health/HealthList.vue') },
      { path: 'health/create', name: 'HealthCreate', component: () => import('@/views/health/HealthForm.vue'), meta: { doctorOnly: true } },
      { path: 'health/:id/edit', name: 'HealthEdit', component: () => import('@/views/health/HealthForm.vue'), meta: { doctorOnly: true } }
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  useAuthStore().initFromToken()
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) return next('/login')
  if (to.meta.guest && auth.isLoggedIn) return next('/')
  if (to.meta.doctorOnly && !auth.isDoctor) return next('/')
  next()
})

export default router
