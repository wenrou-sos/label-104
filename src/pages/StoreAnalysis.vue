<template>
  <div class="store-analysis">
    <div class="kpi-cards">
      <a-card class="kpi-card gradient-1">
        <div class="kpi-content">
          <div class="kpi-icon">
            <DollarOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">月度营收</div>
            <div class="kpi-value">¥{{ formatNumber(totalRevenue) }}</div>
            <div class="kpi-trend up">
              <ArrowUpOutlined /> 12.5%
            </div>
          </div>
        </div>
      </a-card>

      <a-card class="kpi-card gradient-2">
        <div class="kpi-content">
          <div class="kpi-icon">
            <ShoppingCartOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">客单价</div>
            <div class="kpi-value">¥{{ avgCustomerPrice }}</div>
            <div class="kpi-trend up">
              <ArrowUpOutlined /> 5.2%
            </div>
          </div>
        </div>
      </a-card>

      <a-card class="kpi-card gradient-3">
        <div class="kpi-content">
          <div class="kpi-icon">
            <ReconciliationOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">到店频次</div>
            <div class="kpi-value">{{ avgVisitFrequency }} 次/月</div>
            <div class="kpi-trend up">
              <ArrowUpOutlined /> 3.8%
            </div>
          </div>
        </div>
      </a-card>

      <a-card class="kpi-card gradient-4">
        <div class="kpi-content">
          <div class="kpi-icon">
            <UserAddOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">新客数</div>
            <div class="kpi-value">{{ totalNewCustomers }} 人</div>
            <div class="kpi-trend down">
              <ArrowDownOutlined /> 2.1%
            </div>
          </div>
        </div>
      </a-card>

      <a-card class="kpi-card gradient-5">
        <div class="kpi-content">
          <div class="kpi-icon">
            <ReloadOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">复购率</div>
            <div class="kpi-value">{{ (avgRepeatRate * 100).toFixed(1) }}%</div>
            <div class="kpi-trend up">
              <ArrowUpOutlined /> 4.6%
            </div>
          </div>
        </div>
      </a-card>
    </div>

    <div class="chart-section">
      <a-card title="门店排名对比" class="ranking-card">
        <template #extra>
          <a-select
            v-model:value="sortField"
            style="width: 140px"
            size="small"
            @change="handleSortChange"
          >
            <a-select-option value="revenue">按营收</a-select-option>
            <a-select-option value="customerPrice">按客单价</a-select-option>
            <a-select-option value="visitFrequency">按到店频次</a-select-option>
            <a-select-option value="newCustomers">按新客数</a-select-option>
            <a-select-option value="repeatRate">按复购率</a-select-option>
          </a-select>
        </template>
        <a-table
          :columns="rankingColumns"
          :data-source="sortedRankingData"
          :pagination="false"
          size="middle"
          row-key="storeId"
        >
          <template #bodyCell="{ column, record, index }">
            <template v-if="column.key === 'rank'">
              <a-badge
                :number="index + 1"
                :color="index < 3 ? '#E8A0BF' : '#ccc'"
                :style="{ backgroundColor: index < 3 ? '#E8A0BF' : '#999' }"
              >
                <span></span>
              </a-badge>
            </template>
            <template v-else-if="column.key === 'revenue'">
              ¥{{ formatNumber(record.revenue) }}
            </template>
            <template v-else-if="column.key === 'customerPrice'">
              ¥{{ record.customerPrice }}
            </template>
            <template v-else-if="column.key === 'visitFrequency'">
              {{ record.visitFrequency }} 次
            </template>
            <template v-else-if="column.key === 'repeatRate'">
              {{ (record.repeatRate * 100).toFixed(1) }}%
            </template>
          </template>
        </a-table>
      </a-card>

      <a-card title="营收趋势对比" class="trend-card">
        <PlotlyChart
          :data="trendChartData"
          :layout="trendChartLayout"
          height="380px"
        />
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import {
  DollarOutlined,
  ShoppingCartOutlined,
  ReconciliationOutlined,
  UserAddOutlined,
  ReloadOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons-vue'
import PlotlyChart from '@/components/charts/PlotlyChart.vue'
import { storeApi } from '@/api/store'
import { useFilter } from '@/composables/useFilter'
import type { StoreMetric } from '@/types'

const { filterParams } = useFilter()

const metricsData = ref<StoreMetric[]>([])
const trendData = ref<any[]>([])
const sortField = ref('revenue')

const rankingColumns = [
  { title: '排名', key: 'rank', width: 80, align: 'center' },
  { title: '门店名称', dataIndex: 'storeName', key: 'storeName' },
  { title: '月度营收', dataIndex: 'revenue', key: 'revenue', sorter: true },
  { title: '客单价', dataIndex: 'customerPrice', key: 'customerPrice', sorter: true },
  { title: '到店频次', dataIndex: 'visitFrequency', key: 'visitFrequency', sorter: true },
  { title: '新客数', dataIndex: 'newCustomers', key: 'newCustomers', sorter: true },
  { title: '复购率', dataIndex: 'repeatRate', key: 'repeatRate', sorter: true },
]

const totalRevenue = computed(() =>
  metricsData.value.reduce((sum, item) => sum + item.revenue, 0)
)

const avgCustomerPrice = computed(() => {
  if (metricsData.value.length === 0) return 0
  return Math.round(
    metricsData.value.reduce((sum, item) => sum + item.customerPrice, 0) /
      metricsData.value.length
  )
})

const avgVisitFrequency = computed(() => {
  if (metricsData.value.length === 0) return 0
  return (
    metricsData.value.reduce((sum, item) => sum + item.visitFrequency, 0) /
    metricsData.value.length
  ).toFixed(1)
})

const totalNewCustomers = computed(() =>
  metricsData.value.reduce((sum, item) => sum + item.newCustomers, 0)
)

const avgRepeatRate = computed(() => {
  if (metricsData.value.length === 0) return 0
  return (
    metricsData.value.reduce((sum, item) => sum + item.repeatRate, 0) /
    metricsData.value.length
  )
})

const sortedRankingData = computed(() => {
  const data = [...metricsData.value]
  const field = sortField.value as keyof StoreMetric
  return data.sort((a, b) => {
    const aVal = a[field] as number
    const bVal = b[field] as number
    return bVal - aVal
  })
})

const chartColors = ['#E8A0BF', '#6B5B95', '#F5C6A5', '#A7D8B0', '#B8C5E0']

const trendChartData = computed(() => {
  if (trendData.value.length === 0) return []

  const storeNames = [...new Set(trendData.value.flatMap(d => d.stores.map((s: any) => s.storeName)))]
  
  return storeNames.map((storeName, idx) => {
    const values = trendData.value.map(d => {
      const store = d.stores.find((s: any) => s.storeName === storeName)
      return store ? store.revenue : 0
    })

    return {
      x: trendData.value.map(d => d.date),
      y: values,
      type: 'scatter',
      mode: 'lines+markers',
      name: storeName,
      line: {
        color: chartColors[idx % chartColors.length],
        width: 3,
        shape: 'spline',
      },
      marker: {
        size: 6,
        color: chartColors[idx % chartColors.length],
      },
      hovertemplate: '%{x}<br>营收: ¥%{y:,.0f}<extra></extra>',
    }
  })
})

const trendChartLayout = {
  margin: { l: 60, r: 30, t: 20, b: 40 },
  xaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
  },
  yaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    tickformat: ',.0f',
    title: {
      text: '营收 (元)',
      font: { size: 12, color: '#666' },
    },
  },
  legend: {
    orientation: 'h',
    y: -0.15,
    x: 0,
  },
  hovermode: 'x unified',
}

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

function handleSortChange() {
}

async function loadData() {
  try {
    const [metrics, trend] = await Promise.all([
      storeApi.getStoreMetrics(filterParams.value),
      storeApi.getStoreTrend(filterParams.value),
    ])
    metricsData.value = metrics
    trendData.value = trend
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

watch(
  () => filterParams.value,
  () => {
    loadData()
  },
  { deep: true }
)

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.store-analysis {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.kpi-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.kpi-card {
  border: none !important;
  overflow: hidden;
}

.kpi-card :deep(.ant-card-body) {
  padding: 20px !important;
}

.gradient-1 {
  background: linear-gradient(135deg, #FCE7F3 0%, #FBCFE8 100%);
}

.gradient-2 {
  background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);
}

.gradient-3 {
  background: linear-gradient(135deg, #FFF0E6 0%, #FFE4D1 100%);
}

.gradient-4 {
  background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
}

.gradient-5 {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
}

.kpi-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.kpi-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #6B5B95;
}

.kpi-info {
  flex: 1;
}

.kpi-label {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

.kpi-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.kpi-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 2px;
}

.kpi-trend.up {
  color: #52c41a;
}

.kpi-trend.down {
  color: #ff4d4f;
}

.chart-section {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
}

.ranking-card {
  min-height: 420px;
}

.trend-card {
  min-height: 420px;
}

@media (max-width: 1200px) {
  .kpi-cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .kpi-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .chart-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .kpi-cards {
    grid-template-columns: 1fr;
  }
}
</style>
