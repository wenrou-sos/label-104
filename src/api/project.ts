import { http } from './request'
import { mockData } from './mock'
import type { ProjectSales, ProjectMatrix, ProjectMargin, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

const QUADRANT_MAP: Record<string, number> = {
  q1: 1, // 明星
  q2: 2, // 问题
  q3: 3, // 瘦狗
  q4: 4, // 现金牛
  star: 1,
  question: 2,
  dog: 3,
  cash_cow: 4,
}

export function getProjectSales(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<ProjectSales[]>('/projects/sales', params),
    mockData.projectSales
  ).then((list: any) => {
    if (!Array.isArray(list)) return list
    return list.map((item: any) => ({
      ...item,
      salesCount: item.salesCount ?? 0,
      salesAmount: item.salesAmount ?? 0,
      salesRatio: item.salesRatio ?? 0,
    }))
  })
}

export function getProjectMargin(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}): Promise<ProjectMargin[]> {
  return withFallback<any>(
    http.get<any>('/projects/margin', params),
    mockData.projectMargins as any
  ).then((list: any) => {
    if (!Array.isArray(list)) return [] as ProjectMargin[]
    return list.map((item: any) => {
      const grossMarginRate = Number(item.grossMargin ?? item.grossMarginRate ?? 0)
      const grossProfit = Number(item.grossProfit ?? item.grossMargin ?? 0)
      return {
        projectId: item.projectId,
        projectName: item.projectName,
        category: item.category,
        salesCount: Number(item.salesCount ?? 0),
        salesAmount: Number(item.salesAmount ?? 0),
        grossMargin: grossProfit,
        grossMarginRate,
        price: item.price,
        cost: item.cost,
        totalCost: item.totalCost,
      } as ProjectMargin
    })
  })
}

export function getProjectMatrix(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}): Promise<ProjectMatrix[]> {
  return withFallback<any>(
    http.get<any>('/projects/matrix', params),
    { projects: mockData.projectMatrix } as any
  ).then((raw: any) => {
    let projects: any[] = []
    if (Array.isArray(raw)) {
      projects = raw
    } else if (raw && Array.isArray(raw.projects)) {
      projects = raw.projects
    }
    return projects.map((p: any) => ({
      projectId: p.projectId,
      projectName: p.projectName,
      category: p.category,
      salesAmount: Number(p.salesAmount ?? 0),
      grossMarginRate: Number(p.grossMargin ?? p.grossMarginRate ?? 0),
      quadrant:
        typeof p.quadrant === 'number'
          ? p.quadrant
          : QUADRANT_MAP[p.quadrant] ?? 3,
    })) as ProjectMatrix[]
  })
}

export const projectApi = {
  getProjectSales,
  getProjectMargin,
  getProjectMatrix,
}

export default projectApi
