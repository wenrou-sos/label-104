import { http } from './request'
import { mockData } from './mock'
import type { Store, StoreMetric, StoreTrendData, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

export function getStores() {
  return withFallback(http.get<Store[]>('/stores'), mockData.stores)
}

export function getStoreMetrics(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<StoreMetric[]>('/stores/metrics', params),
    mockData.storeMetrics
  )
}

export function getStoreRanking(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
  sortBy?: string
  sortOrder?: string
}) {
  return withFallback(
    http.get<StoreMetric[]>('/stores/ranking', params),
    [...mockData.storeMetrics].sort((a, b) => b.revenue - a.revenue)
  )
}

export function getStoreTrend(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<StoreTrendData[]>('/stores/trend', params),
    mockData.trendData
  )
}

export const storeApi = {
  getStores,
  getStoreMetrics,
  getStoreRanking,
  getStoreTrend,
}

export default storeApi
