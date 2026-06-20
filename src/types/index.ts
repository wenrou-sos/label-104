export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface Store {
  storeId: string
  storeName: string
  city: string
  area: string
  openDate: string
}

export interface StoreMetric {
  storeId: string
  storeName: string
  statDate: string
  revenue: number
  customerPrice: number
  visitFrequency: number
  newCustomers: number
  repeatRate: number
}

export interface StoreTrendData {
  date: string
  stores: {
    storeId: string
    storeName: string
    revenue: number
    customerPrice: number
    visitFrequency: number
    newCustomers: number
    repeatRate: number
  }[]
}

export interface Project {
  projectId: string
  projectName: string
  category: string
  price: number
  cost: number
}

export interface ProjectSales {
  projectId: string
  projectName: string
  category: string
  salesCount: number
  salesAmount: number
  salesRatio: number
}

export interface ProjectMargin {
  projectId: string
  projectName: string
  category: string
  salesCount: number
  salesAmount: number
  grossMargin: number
  grossMarginRate: number
  price?: number
  cost?: number
  totalCost?: number
}

export interface ProjectMatrix {
  projectId: string
  projectName: string
  category?: string
  salesAmount: number
  grossMarginRate: number
  quadrant: number
}

export interface Employee {
  empId: string
  empName: string
  storeId: string
  storeName: string
  position: string
  serviceType: string
}

export interface EmployeeRanking {
  empId: string
  empName: string
  storeName: string
  serviceType: string
  cardAmount: number
  orderCount: number
  avgPrice: number
  rank: number
}

export interface EmployeeOrderData {
  empId: string
  empName: string
  orderCount: number
  avgPrice: number
}

export interface Member {
  memberId: string
  storeId: string
  storeName: string
  registerDate: string
  totalRecharge: number
  lastVisitDate: string
  totalVisits: number
  rechargeCycleDays: number
  rechargedIn90d: boolean
}

export interface MemberCycleStats {
  avgRechargeCycle: number
  rechargeRate: number
  totalMembers: number
  activeMembers: number
  newMembers: number
}

export interface ChurnMember {
  memberId: string
  memberName: string
  storeName: string
  lastVisitDate: string
  daysSinceLastVisit: number
  totalRecharge: number
  totalVisits: number
  level: 'high' | 'medium' | 'low'
}

export interface ChurnResponse {
  total: number
  list: ChurnMember[]
}

export interface Channel {
  channelId: string
  channelName: string
  channelType: string
}

export interface ChannelConversion {
  channelId: string
  channelName: string
  channelType: string
  exposureCount: number
  clickCount: number
  arrivalCount: number
  conversionRate: number
  clickRate: number
}

export interface ChannelAov {
  channelId: string
  channelName: string
  avgPrice: number
  totalRevenue: number
  customerCount: number
}

export interface ChannelEvaluation {
  channelId: string
  channelName: string
  conversionScore: number
  revenueScore: number
  costScore: number
  totalScore: number
  suggestion: string
}

export interface FilterOptions {
  startDate: string
  endDate: string
  storeIds: string[]
}

export type ServiceType = 'all' | 'beauty' | 'nail' | 'spa' | 'hair'
