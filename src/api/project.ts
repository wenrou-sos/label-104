import { http } from './request'
import { mockData } from './mock'
import type { ProjectSales, ProjectMatrix, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

export function getProjectSales(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<ProjectSales[]>('/projects/sales', params),
    mockData.projectSales
  )
}

export function getProjectMargin(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<ProjectSales[]>('/projects/margin', params),
    mockData.projectSales
  )
}

export function getProjectMatrix(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<ProjectMatrix[]>('/projects/matrix', params),
    mockData.projectMatrix
  )
}

export const projectApi = {
  getProjectSales,
  getProjectMargin,
  getProjectMatrix,
}

export default projectApi
