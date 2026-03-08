import request from './request'

export const login = async (data) => await request.post('/users/login', data)
export const register = async (data) => await request.post('/users/register', data)
