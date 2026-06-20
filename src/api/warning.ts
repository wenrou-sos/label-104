import { http } from './request'
import type { WarningConfig, ApiResponse } from '@/types'

const DEFAULT_CONFIG: WarningConfig = {
  storeRevenueDropThreshold: 10.0,
  memberChurnDaysThreshold: 60,
  memberChurnHighRiskDays: 120,
  memberChurnMediumRiskDays: 90,
}

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

export function getWarningConfig(): Promise<WarningConfig> {
  return withFallback<WarningConfig>(
    http.get<WarningConfig>('/warnings/config'),
    DEFAULT_CONFIG
  )
}

export async function saveWarningConfig(config: Partial<WarningConfig>): Promise<WarningConfig> {
  const res = await http.post<WarningConfig>('/warnings/config', config)
  return res.data
}

export const warningApi = {
  getWarningConfig,
  saveWarningConfig,
}

export default warningApi
