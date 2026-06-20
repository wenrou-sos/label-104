import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/store-analysis',
  },
  {
    path: '/store-analysis',
    name: 'store-analysis',
    component: () => import('@/pages/StoreAnalysis.vue'),
    meta: { title: '门店核心指标', icon: 'ShopOutlined' },
  },
  {
    path: '/project-analysis',
    name: 'project-analysis',
    component: () => import('@/pages/ProjectAnalysis.vue'),
    meta: { title: '项目分析', icon: 'PieChartOutlined' },
  },
  {
    path: '/employee-analysis',
    name: 'employee-analysis',
    component: () => import('@/pages/EmployeeAnalysis.vue'),
    meta: { title: '员工产出分析', icon: 'TeamOutlined' },
  },
  {
    path: '/member-lifecycle',
    name: 'member-lifecycle',
    component: () => import('@/pages/MemberLifecycle.vue'),
    meta: { title: '会员生命周期', icon: 'HeartOutlined' },
  },
  {
    path: '/channel-analysis',
    name: 'channel-analysis',
    component: () => import('@/pages/ChannelAnalysis.vue'),
    meta: { title: '渠道获客分析', icon: 'ShareAltOutlined' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
