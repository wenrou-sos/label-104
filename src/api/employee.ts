import { http } from './request'
import { mockData } from './mock'
import type { EmployeeRanking, EmployeeOrderData, EmployeeTrendResponse, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

export function getEmployeeRanking(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
  serviceType?: string
}) {
  let data = mockData.employeeRankings
  if (params?.serviceType && params.serviceType !== 'all') {
    const typeMap: Record<string, string> = {
      beauty: '美容',
      nail: '美甲',
      spa: 'SPA',
      hair: '美发',
    }
    data = data.filter(e => e.serviceType === typeMap[params.serviceType])
  }
  return withFallback(
    http.get<EmployeeRanking[]>('/employees/ranking', params),
    data
  )
}

export function getEmployeeOrders(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
  serviceType?: string
}) {
  let data = mockData.employeeOrderData
  if (params?.serviceType && params.serviceType !== 'all') {
    const typeMap: Record<string, string> = {
      beauty: '美容',
      nail: '美甲',
      spa: 'SPA',
      hair: '美发',
    }
    const filteredRankings = mockData.employeeRankings.filter(
      e => e.serviceType === typeMap[params.serviceType]
    )
    data = filteredRankings.map(e => ({
      empId: e.empId,
      empName: e.empName,
      orderCount: e.orderCount,
      avgPrice: e.avgPrice,
    }))
  }
  return withFallback(
    http.get<EmployeeOrderData[]>('/employees/orders', params),
    data
  )
}

export function getEmployeeTrend(empId: string, months: number = 6): Promise<EmployeeTrendResponse> {
  return withFallback<EmployeeTrendResponse>(
    http.get<EmployeeTrendResponse>(`/employees/trend/${empId}`, { months }),
    { employee: null, trend: [] }
  )
}

export const employeeApi = {
  getEmployeeRanking,
  getEmployeeOrders,
  getEmployeeTrend,
}

export default employeeApi
