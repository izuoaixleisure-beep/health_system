import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin } from '@/api/user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const isDoctor = computed(() => user.value?.role === 'doctor')
  const isResident = computed(() => user.value?.role === 'resident')

  function setAuth(t) {
    token.value = t
    localStorage.setItem('token', t)
    if (t) {
      const payload = JSON.parse(atob(t.split('.')[1]))
      user.value = { username: payload.sub, role: payload.role, resident_id: payload.resident_id }
    } else {
      user.value = null
    }
  }

  function clearUser() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  async function login(data) {
    const res = await apiLogin(data)
    setAuth(res.access_token)
    return res
  }

  function initFromToken() {
    const t = localStorage.getItem('token')
    if (t) setAuth(t)
  }

  return { token, user, isLoggedIn, isDoctor, isResident, setAuth, clearUser, login, initFromToken }
})
