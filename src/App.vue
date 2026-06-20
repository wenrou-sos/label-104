<template>
  <a-layout class="h-screen">
    <a-layout-sider v-model:collapsed="collapsed" collapsible width="220" class="sidebar">
      <div class="logo-container">
        <div class="logo-icon">
          <SmileOutlined :style="{ fontSize: collapsed ? '20px' : '28px', color: '#E8A0BF' }" />
        </div>
        <span v-if="!collapsed" class="logo-text">美颜数据看板</span>
      </div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        mode="inline"
        :theme="'light'"
        @click="handleMenuClick"
      >
        <a-menu-item key="/store-analysis">
          <template #icon>
            <ShopOutlined />
          </template>
          <span>门店核心指标</span>
        </a-menu-item>
        <a-menu-item key="/project-analysis">
          <template #icon>
            <PieChartOutlined />
          </template>
          <span>项目分析</span>
        </a-menu-item>
        <a-menu-item key="/employee-analysis">
          <template #icon>
            <TeamOutlined />
          </template>
          <span>员工产出分析</span>
        </a-menu-item>
        <a-menu-item key="/member-lifecycle">
          <template #icon>
            <HeartOutlined />
          </template>
          <span>会员生命周期</span>
        </a-menu-item>
        <a-menu-item key="/channel-analysis">
          <template #icon>
            <ShareAltOutlined />
          </template>
          <span>渠道获客分析</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout class="main-layout">
      <a-layout-header class="header">
        <div class="header-content">
          <div class="page-title">{{ currentPageTitle }}</div>
          <div class="filter-bar">
            <div class="filter-item">
              <span class="filter-label">时间范围</span>
              <a-range-picker
                v-model:value="dateRange"
                format="YYYY-MM-DD"
                style="width: 260px"
                @change="handleDateChange"
              />
            </div>
            <div class="filter-item">
              <span class="filter-label">门店</span>
              <a-select
                v-model:value="selectedStoreIds"
                mode="multiple"
                :options="storeOptions"
                placeholder="请选择门店"
                style="min-width: 200px"
                max-tag-count="3"
              />
            </div>
          </div>
        </div>
      </a-layout-header>

      <a-layout-content class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ShopOutlined,
  PieChartOutlined,
  TeamOutlined,
  HeartOutlined,
  ShareAltOutlined,
  SmileOutlined,
} from '@ant-design/icons-vue'
import { useFilter } from '@/composables/useFilter'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const { startDate, endDate, selectedStoreIds, storeOptions, loadStores } = useFilter()

const collapsed = ref(false)
const selectedKeys = ref<string[]>([route.path])

const dateRange = ref<[dayjs.Dayjs, dayjs.Dayjs]>([
  dayjs('2024-01-01'),
  dayjs('2024-06-30'),
])

const currentPageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/store-analysis': '门店核心指标',
    '/project-analysis': '项目分析',
    '/employee-analysis': '员工产出分析',
    '/member-lifecycle': '会员生命周期',
    '/channel-analysis': '渠道获客分析',
  }
  return titles[route.path] || '数据分析'
})

function handleMenuClick({ key }: { key: string }) {
  router.push(key)
}

function handleDateChange(dates: any) {
  if (dates && dates.length === 2) {
    startDate.value = dates[0].format('YYYY-MM-DD')
    endDate.value = dates[1].format('YYYY-MM-DD')
  }
}

onMounted(() => {
  loadStores()
})
</script>

<style scoped>
.sidebar {
  background: #fff;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
}

.logo-container {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #6B5B95;
  white-space: nowrap;
}

.main-layout {
  background: transparent;
  overflow: hidden;
}

.header {
  background: #fff;
  padding: 0;
  height: auto;
  line-height: normal;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  z-index: 10;
}

.header-content {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #6B5B95;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}

.content {
  padding: 24px;
  overflow-y: auto;
  background: transparent;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:deep(.ant-layout-sider-trigger) {
  background: #fff;
  color: #E8A0BF;
  border-top: 1px solid #f0f0f0;
}

:deep(.ant-menu) {
  border-right: none;
}

:deep(.ant-menu-item) {
  margin: 4px 8px;
  border-radius: 8px;
}

:deep(.ant-menu-item-selected) {
  background: linear-gradient(90deg, rgba(232, 160, 191, 0.2) 0%, rgba(232, 160, 191, 0.05) 100%) !important;
  color: #E8A0BF !important;
}

:deep(.ant-menu-item-selected::after) {
  display: none;
}
</style>
