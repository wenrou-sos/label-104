import { http } from './request'
import { mockData } from './mock'
import type { MemberCycleStats, ChurnMember, ChurnResponse, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

interface MemberCycleRaw {
  avgRechargeCycle: number
  rechargeRate: number
  totalMembers: number
  activeMembers: number
  newMembers?: number
  distribution?: Array<{ label: string; count: number; ratio: number }>
  stores?: Array<{ storeId: string; storeName: string; avgCycleDays: number; memberCount: number }>
}

export function getMemberCycle(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback<MemberCycleRaw>(
    http.get<MemberCycleRaw>('/members/cycle', params),
    mockData.memberCycleStats as unknown as MemberCycleRaw
  ).then((raw): MemberCycleStats => {
    if (raw && typeof raw.avgRechargeCycle === 'number') {
      return {
        avgRechargeCycle: Number(raw.avgRechargeCycle) || 0,
        rechargeRate: Number(raw.rechargeRate) || 0,
        totalMembers: Number(raw.totalMembers) || 0,
        activeMembers: Number(raw.activeMembers) || 0,
        newMembers: Number(raw.newMembers) || 0,
      }
    }
    return mockData.memberCycleStats
  })
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

function normaliseChurnList(raw: any): ChurnMember[] {
  const list = Array.isArray(raw) ? raw : (raw && raw.list) || []
  return list.map((item: any): ChurnMember => ({
    memberId: String(item.memberId ?? ''),
    memberName: String(item.memberName ?? '未知'),
    storeName: String(item.storeName ?? ''),
    lastVisitDate: String(item.lastVisitDate ?? ''),
    daysSinceLastVisit: Number(item.daysSinceLastVisit) || 0,
    totalRecharge: Number(item.totalRecharge) || 0,
    totalVisits: Number(item.totalVisits) || 0,
    level: (item.level === 'high' || item.level === 'medium' || item.level === 'low') ? item.level : 'low',
  }))
}

export function getChurnMembers(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
  days?: number
}) {
  return withFallback<ChurnResponse | ChurnMember[]>(
    http.get<ChurnResponse | ChurnMember[]>('/members/churn', params),
    mockData.churnMembers
  ).then(raw => {
    const list = normaliseChurnList(raw)
    let total: number
    if (raw && !Array.isArray(raw) && typeof raw.total === 'number') {
      total = raw.total
    } else {
      total = list.length
    }
    return { total, list } as ChurnResponse
  })
}

export const memberApi = {
  getMemberCycle,
  getMemberRecharge,
  getChurnMembers,
}

export default memberApi
