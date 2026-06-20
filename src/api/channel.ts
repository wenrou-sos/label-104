import { http } from './request'
import { mockData } from './mock'
import type { ChannelConversion, ChannelAov, ChannelEvaluation, ApiResponse } from '@/types'

async function withFallback<T>(apiCall: Promise<ApiResponse<T>>, fallback: T): Promise<T> {
  try {
    const res = await apiCall
    return res.data
  } catch {
    return fallback
  }
}

export function getChannelConversion(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<ChannelConversion[]>('/channels/conversion', params),
    mockData.channelConversions
  )
}

export function getChannelAov(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<ChannelAov[]>('/channels/aov', params),
    mockData.channelAovs
  )
}

export function getChannelEvaluation(params?: {
  startDate?: string
  endDate?: string
  storeIds?: string
}) {
  return withFallback(
    http.get<ChannelEvaluation[]>('/channels/evaluation', params),
    mockData.channelEvaluations
  )
}

export const channelApi = {
  getChannelConversion,
  getChannelAov,
  getChannelEvaluation,
}

export default channelApi
