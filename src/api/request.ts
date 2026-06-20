import type { ApiResponse } from '@/types'
import { snakeToCamel } from '@/lib/utils'

const BASE_URL = '/api/v1'

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  params?: Record<string, any>
  body?: any
  headers?: Record<string, string>
}

async function request<T>(
  url: string,
  options: RequestOptions = {}
): Promise<ApiResponse<T>> {
  const { method = 'GET', params, body, headers = {} } = options

  let fullUrl = BASE_URL + url

  if (params && Object.keys(params).length > 0) {
    const searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value))
      }
    })
    fullUrl += `?${searchParams.toString()}`
  }

  try {
    const response = await fetch(fullUrl, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    })

    const data = await response.json()

    if (data.code !== 200) {
      throw new Error(data.message || '请求失败')
    }

    return snakeToCamel(data)
  } catch (error) {
    console.error('Request error:', error)
    throw error
  }
}

export const http = {
  get: <T>(url: string, params?: Record<string, any>) =>
    request<T>(url, { method: 'GET', params }),
  post: <T>(url: string, body?: any) =>
    request<T>(url, { method: 'POST', body }),
  put: <T>(url: string, body?: any) =>
    request<T>(url, { method: 'PUT', body }),
  delete: <T>(url: string, params?: Record<string, any>) =>
    request<T>(url, { method: 'DELETE', params }),
}

export default http
