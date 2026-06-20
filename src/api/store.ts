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

export interface StoreTrendRaw {
  months: string[]
  stores: {
    storeId: string
    storeName: string
    revenues: number[]
    customerPrices: number[]
    visitFrequencies: number[]
    newCustomers: number[]
    repeatRates?: number[]
  }[]
}

export function getStoreTrend(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}): Promise<StoreTrendData[]> {
  return withFallback<StoreTrendRaw>(
    http.get<StoreTrendRaw>('/stores/trend', params),
    mockData.trendData as unknown as StoreTrendRaw
  ).then((raw: any) => {
    if (Array.isArray(raw)) return raw
    const months = raw.months || []
    const stores = raw.stores || []
    return months.map((month: string, idx: number) => ({
      date: month,
      stores: stores.map((s: any) => ({
        storeId: s.storeId,
        storeName: s.storeName,
        revenue: s.revenues?.[idx] ?? 0,
        customerPrice: s.customerPrices?.[idx] ?? 0,
        visitFrequency: s.visitFrequencies?.[idx] ?? 0,
        newCustomers: s.newCustomers?.[idx] ?? 0,
        repeatRate: s.repeatRates?.[idx] ?? 0,
      })),
    }))
  }) as Promise<StoreTrendData[]>
}

export const storeApi = {
  getStores,
  getStoreMetrics,
  getStoreRanking,
  getStoreTrend,
}

export default storeApi
