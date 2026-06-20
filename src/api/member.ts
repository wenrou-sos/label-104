import { http } from './request'
import { mockData } from './mock'
import type { MemberCycleStats, ChurnMember, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

export function getMemberCycle(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<MemberCycleStats>('/members/cycle', params),
    mockData.memberCycleStats
  )
}

export function getMemberRecharge(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<{ rechargeRate: number; avgRechargeAmount: number }>('/members/recharge', params),
    {
      rechargeRate: mockData.memberCycleStats.rechargeRate,
      avgRechargeAmount: 3500,
    }
  )
}

export function getChurnMembers(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
  days?: number
}) {
  return withFallback(
    http.get<ChurnMember[]>('/members/churn', params),
    mockData.churnMembers
  )
}

export const memberApi = {
  getMemberCycle,
  getMemberRecharge,
  getChurnMembers,
}

export default memberApi
