import type {
  Store,
  StoreMetric,
  StoreTrendData,
  ProjectSales,
  ProjectMargin,
  ProjectMatrix,
  EmployeeRanking,
  EmployeeOrderData,
  MemberCycleStats,
  ChurnMember,
  ChannelConversion,
  ChannelAov,
  ChannelEvaluation,
} from '@/types'

const stores: Store[] = [
  { storeId: 'S001', storeName: '朝阳门店', city: '北京', area: '朝阳区', openDate: '2022-03-15' },
  { storeId: 'S002', storeName: '海淀店', city: '北京', area: '海淀区', openDate: '2022-06-20' },
  { storeId: 'S003', storeName: '浦东店', city: '上海', area: '浦东新区', openDate: '2023-01-10' },
  { storeId: 'S004', storeName: '徐汇店', city: '上海', area: '徐汇区', openDate: '2023-05-08' },
  { storeId: 'S005', storeName: '天河店', city: '广州', area: '天河区', openDate: '2023-08-12' },
]

const storeMetrics: StoreMetric[] = [
  { storeId: 'S001', storeName: '朝阳门店', statDate: '2024-06', revenue: 586000, customerPrice: 680, visitFrequency: 2.8, newCustomers: 156, repeatRate: 0.72 },
  { storeId: 'S002', storeName: '海淀店', statDate: '2024-06', revenue: 523000, customerPrice: 620, visitFrequency: 2.5, newCustomers: 142, repeatRate: 0.68 },
  { storeId: 'S003', storeName: '浦东店', statDate: '2024-06', revenue: 612000, customerPrice: 720, visitFrequency: 3.1, newCustomers: 168, repeatRate: 0.75 },
  { storeId: 'S004', storeName: '徐汇店', statDate: '2024-06', revenue: 478000, customerPrice: 590, visitFrequency: 2.3, newCustomers: 125, repeatRate: 0.65 },
  { storeId: 'S005', storeName: '天河店', statDate: '2024-06', revenue: 445000, customerPrice: 560, visitFrequency: 2.2, newCustomers: 118, repeatRate: 0.62 },
]

function generateTrendData(): StoreTrendData[] {
  const months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']
  return months.map(month => ({
    date: month,
    stores: stores.map((store, idx) => {
      const baseRevenue = 400000 + idx * 50000
      const variance = (Math.random() - 0.5) * 0.3
      return {
        storeId: store.storeId,
        storeName: store.storeName,
        revenue: Math.round(baseRevenue * (1 + variance)),
        customerPrice: Math.round(550 + idx * 30 + (Math.random() - 0.5) * 50),
        visitFrequency: +(2.0 + idx * 0.2 + (Math.random() - 0.5) * 0.5).toFixed(1),
        newCustomers: Math.round(100 + idx * 15 + (Math.random() - 0.5) * 30),
        repeatRate: +(0.55 + idx * 0.04 + (Math.random() - 0.5) * 0.1).toFixed(2),
      }
    }),
  }))
}

const projectSales: ProjectSales[] = [
  { projectId: 'P001', projectName: '面部护理套餐', category: '美容', salesCount: 320, salesAmount: 256000, salesRatio: 0.24 },
  { projectId: 'P002', projectName: '美甲系列', category: '美甲', salesCount: 450, salesAmount: 135000, salesRatio: 0.13 },
  { projectId: 'P003', projectName: 'SPA水疗', category: 'SPA', salesCount: 180, salesAmount: 198000, salesRatio: 0.19 },
  { projectId: 'P004', projectName: '美发造型', category: '美发', salesCount: 280, salesAmount: 84000, salesRatio: 0.08 },
  { projectId: 'P005', projectName: '身体护理', category: '美容', salesCount: 220, salesAmount: 176000, salesRatio: 0.17 },
  { projectId: 'P006', projectName: '美睫嫁接', category: '美甲', salesCount: 310, salesAmount: 93000, salesRatio: 0.09 },
  { projectId: 'P007', projectName: '光子嫩肤', category: '美容', salesCount: 95, salesAmount: 142500, salesRatio: 0.13 },
  { projectId: 'P008', projectName: '艾灸养生', category: 'SPA', salesCount: 160, salesAmount: 72000, salesRatio: 0.07 },
]

const projectMargins: ProjectMargin[] = [
  { projectId: 'P001', projectName: '面部护理套餐', category: '美容', salesCount: 320, salesAmount: 256000, grossMargin: 153600, grossMarginRate: 0.6 },
  { projectId: 'P002', projectName: '美甲系列', category: '美甲', salesCount: 450, salesAmount: 135000, grossMargin: 94500, grossMarginRate: 0.7 },
  { projectId: 'P003', projectName: 'SPA水疗', category: 'SPA', salesCount: 180, salesAmount: 198000, grossMargin: 99000, grossMarginRate: 0.5 },
  { projectId: 'P004', projectName: '美发造型', category: '美发', salesCount: 280, salesAmount: 84000, grossMargin: 42000, grossMarginRate: 0.5 },
  { projectId: 'P005', projectName: '身体护理', category: '美容', salesCount: 220, salesAmount: 176000, grossMargin: 105600, grossMarginRate: 0.6 },
  { projectId: 'P006', projectName: '美睫嫁接', category: '美甲', salesCount: 310, salesAmount: 93000, grossMargin: 65100, grossMarginRate: 0.7 },
  { projectId: 'P007', projectName: '光子嫩肤', category: '美容', salesCount: 95, salesAmount: 142500, grossMargin: 71250, grossMarginRate: 0.5 },
  { projectId: 'P008', projectName: '艾灸养生', category: 'SPA', salesCount: 160, salesAmount: 72000, grossMargin: 43200, grossMarginRate: 0.6 },
]

const projectMatrix: ProjectMatrix[] = projectMargins.map(p => ({
  projectId: p.projectId,
  projectName: p.projectName,
  category: p.category,
  salesAmount: p.salesAmount,
  grossMarginRate: p.grossMarginRate,
  quadrant: p.salesAmount > 150000 && p.grossMarginRate > 0.55 ? 1 :
            p.salesAmount <= 150000 && p.grossMarginRate > 0.55 ? 2 :
            p.salesAmount <= 150000 && p.grossMarginRate <= 0.55 ? 3 : 4,
}))

const employeeRankings: EmployeeRanking[] = [
  { empId: 'E001', empName: '王美容', storeName: '朝阳门店', serviceType: '美容', cardAmount: 128000, orderCount: 185, avgPrice: 692, rank: 1 },
  { empId: 'E002', empName: '李美甲', storeName: '浦东店', serviceType: '美甲', cardAmount: 115000, orderCount: 220, avgPrice: 523, rank: 2 },
  { empId: 'E003', empName: '张SPA', storeName: '海淀店', serviceType: 'SPA', cardAmount: 102000, orderCount: 145, avgPrice: 703, rank: 3 },
  { empId: 'E004', empName: '赵美发', storeName: '徐汇店', serviceType: '美发', cardAmount: 89000, orderCount: 175, avgPrice: 509, rank: 4 },
  { empId: 'E005', empName: '陈美容', storeName: '天河店', serviceType: '美容', cardAmount: 85000, orderCount: 130, avgPrice: 654, rank: 5 },
  { empId: 'E006', empName: '刘美甲', storeName: '朝阳门店', serviceType: '美甲', cardAmount: 78000, orderCount: 160, avgPrice: 488, rank: 6 },
  { empId: 'E007', empName: '周SPA', storeName: '浦东店', serviceType: 'SPA', cardAmount: 72000, orderCount: 105, avgPrice: 686, rank: 7 },
  { empId: 'E008', empName: '吴美容', storeName: '海淀店', serviceType: '美容', cardAmount: 68000, orderCount: 98, avgPrice: 694, rank: 8 },
]

const employeeOrderData: EmployeeOrderData[] = employeeRankings.map(e => ({
  empId: e.empId,
  empName: e.empName,
  orderCount: e.orderCount,
  avgPrice: e.avgPrice,
}))

const memberCycleStats: MemberCycleStats = {
  avgRechargeCycle: 45,
  rechargeRate: 0.68,
  totalMembers: 5280,
  activeMembers: 3680,
  newMembers: 792,
}

const churnMembers: ChurnMember[] = [
  { memberId: 'M0001', memberName: '张女士', storeName: '朝阳门店', lastVisitDate: '2024-04-10', daysSinceLastVisit: 70, totalRecharge: 15000, totalVisits: 28, level: 'high' },
  { memberId: 'M0002', memberName: '李女士', storeName: '浦东店', lastVisitDate: '2024-04-15', daysSinceLastVisit: 65, totalRecharge: 12000, totalVisits: 22, level: 'high' },
  { memberId: 'M0003', memberName: '王女士', storeName: '海淀店', lastVisitDate: '2024-04-20', daysSinceLastVisit: 60, totalRecharge: 8000, totalVisits: 15, level: 'medium' },
  { memberId: 'M0004', memberName: '赵女士', storeName: '徐汇店', lastVisitDate: '2024-04-25', daysSinceLastVisit: 55, totalRecharge: 6500, totalVisits: 12, level: 'medium' },
  { memberId: 'M0005', memberName: '陈女士', storeName: '天河店', lastVisitDate: '2024-04-28', daysSinceLastVisit: 52, totalRecharge: 5000, totalVisits: 10, level: 'medium' },
  { memberId: 'M0006', memberName: '刘女士', storeName: '朝阳门店', lastVisitDate: '2024-05-01', daysSinceLastVisit: 49, totalRecharge: 3500, totalVisits: 8, level: 'low' },
  { memberId: 'M0007', memberName: '周女士', storeName: '浦东店', lastVisitDate: '2024-05-03', daysSinceLastVisit: 47, totalRecharge: 3000, totalVisits: 7, level: 'low' },
  { memberId: 'M0008', memberName: '吴女士', storeName: '海淀店', lastVisitDate: '2024-05-05', daysSinceLastVisit: 45, totalRecharge: 2500, totalVisits: 6, level: 'low' },
]

const channelConversions: ChannelConversion[] = [
  { channelId: 'C001', channelName: '美团', channelType: '线上平台', exposureCount: 50000, clickCount: 3500, arrivalCount: 420, conversionRate: 0.12, clickRate: 0.07 },
  { channelId: 'C002', channelName: '抖音', channelType: '短视频', exposureCount: 120000, clickCount: 7200, arrivalCount: 580, conversionRate: 0.081, clickRate: 0.06 },
  { channelId: 'C003', channelName: '小红书', channelType: '社交媒体', exposureCount: 80000, clickCount: 6400, arrivalCount: 520, conversionRate: 0.081, clickRate: 0.08 },
  { channelId: 'C004', channelName: '老客推荐', channelType: '口碑', exposureCount: 10000, clickCount: 2000, arrivalCount: 380, conversionRate: 0.19, clickRate: 0.2 },
  { channelId: 'C005', channelName: '微信公众号', channelType: '社交媒体', exposureCount: 30000, clickCount: 3000, arrivalCount: 210, conversionRate: 0.07, clickRate: 0.1 },
  { channelId: 'C006', channelName: '线下活动', channelType: '线下', exposureCount: 5000, clickCount: 1500, arrivalCount: 200, conversionRate: 0.133, clickRate: 0.3 },
]

const channelAovs: ChannelAov[] = [
  { channelId: 'C001', channelName: '美团', avgPrice: 580, totalRevenue: 243600, customerCount: 420 },
  { channelId: 'C002', channelName: '抖音', avgPrice: 420, totalRevenue: 243600, customerCount: 580 },
  { channelId: 'C003', channelName: '小红书', avgPrice: 650, totalRevenue: 338000, customerCount: 520 },
  { channelId: 'C004', channelName: '老客推荐', avgPrice: 880, totalRevenue: 334400, customerCount: 380 },
  { channelId: 'C005', channelName: '微信公众号', avgPrice: 520, totalRevenue: 109200, customerCount: 210 },
  { channelId: 'C006', channelName: '线下活动', avgPrice: 720, totalRevenue: 144000, customerCount: 200 },
]

const channelEvaluations: ChannelEvaluation[] = [
  { channelId: 'C001', channelName: '美团', conversionScore: 75, revenueScore: 70, costScore: 60, totalScore: 68, suggestion: '稳定投放，可尝试拓展新客套餐' },
  { channelId: 'C002', channelName: '抖音', conversionScore: 65, revenueScore: 55, costScore: 50, totalScore: 57, suggestion: '转化率偏低，建议优化落地页和团购套餐' },
  { channelId: 'C003', channelName: '小红书', conversionScore: 70, revenueScore: 80, costScore: 70, totalScore: 73, suggestion: '客单价高，加大达人合作投放' },
  { channelId: 'C004', channelName: '老客推荐', conversionScore: 90, revenueScore: 95, costScore: 95, totalScore: 93, suggestion: '最优渠道，建议加强老带新激励政策' },
  { channelId: 'C005', channelName: '微信公众号', conversionScore: 60, revenueScore: 55, costScore: 75, totalScore: 63, suggestion: '可增加内容营销，提升粉丝活跃度' },
  { channelId: 'C006', channelName: '线下活动', conversionScore: 80, revenueScore: 75, costScore: 55, totalScore: 70, suggestion: '效果不错，可定期举办主题活动' },
]

export const mockData = {
  stores,
  storeMetrics,
  trendData: generateTrendData(),
  projectSales,
  projectMargins,
  projectMatrix,
  employeeRankings,
  employeeOrderData,
  memberCycleStats,
  churnMembers,
  channelConversions,
  channelAovs,
  channelEvaluations,
}

export default mockData
