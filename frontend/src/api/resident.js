import request from './request'

export const getResidents = async (params) => await request.get('/residents/', { params })
export const getResidentById = async (id) => await request.get(`/residents/${id}`)
export const updateResident = async (id, data) => await request.put(`/residents/${id}`, data)
export const deleteResident = async (id) => await request.delete(`/residents/${id}`)
