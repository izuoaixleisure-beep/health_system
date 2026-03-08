import request from './request'

export const getHealthList = async (params) => await request.get('/health/', { params })
export const getHealthById = async (id) => await request.get(`/health/${id}`)
export const createHealth = async (data) => await request.post('/health/', data)
export const updateHealth = async (id, data) => await request.put(`/health/${id}`, data)
export const deleteHealth = async (id) => await request.delete(`/health/${id}`)
