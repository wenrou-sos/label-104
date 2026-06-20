import { http } from './request'
import { mockData } from './mock'
import type { ChannelCostMap, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

export function getAllChannelCosts() {
  return withFallback(
    http.get<ChannelCostMap>('/channel-costs'),
    mockData.channelCosts || {}
  )
}

export function getChannelCostsByPeriod(params?: {
  startDate?: string
  endDate?: string
}) {
  return withFallback(
    http.get<Record<string, number>>('/channel-costs', params),
    {}
  )
}

export function saveChannelCost(channelId: string, statMonth: string, cost: number) {
  return http.post<ChannelCostMap>('/channel-costs', {
    channelId,
    statMonth,
    cost,
  })
}

export function batchSaveChannelCosts(costs: {
  channelId: string
  statMonth: string
  cost: number
}[]) {
  return http.post<ChannelCostMap>('/channel-costs/batch', { costs })
}

export const channelCostApi = {
  getAllChannelCosts,
  getChannelCostsByPeriod,
  saveChannelCost,
  batchSaveChannelCosts,
}

export default channelCostApi
