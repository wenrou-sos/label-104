<template>
  <div class="store-analysis">
    <div class="top-toolbar">
      <div class="toolbar-left">
        <a-tag color="purple" class="mode-tag" v-if="compareMode">对比模式</a-tag>
      </div>
      <div class="toolbar-right">
        <a-space>
          <a-tooltip title="选择 2-3 家门店并排对比 KPI、叠加趋势">
            <a-switch
              v-model:checked="compareMode"
              checked-children="对比"
              un-checked-children="汇总"
              @change="handleCompareModeChange"
            />
          </a-tooltip>
          <a-modal
            v-model:open="compareModalOpen"
            title="选择对比门店"
            :ok-button-props="{ disabled: compareStoreIds.length < 2 }"
            ok-text="开始对比"
            cancel-text="取消"
            @ok="confirmCompareStores"
          >
            <div style="margin-bottom: 8px; color: #666; font-size: 13px">
              请选择 2-3 家门店进行对比，当前已选 <b>{{ compareStoreIds.length }}</b> 家
            </div>
            <a-select
              v-model:value="compareStoreIds"
              mode="multiple"
              :max-tag-count="3"
              placeholder="选择门店（2-3 家）"
              style="width: 100%"
              :options="storeOptions"
              @change="validateCompareSelection"
            />
            <div v-if="compareStoreIds.length > 3" style="color: #ff4d4f; font-size: 12px; margin-top: 6px">
              最多只能选择 3 家门店
            </div>
          </a-modal>
        </a-space>
      </div>
    </div>

    <div v-if="!compareMode" class="kpi-cards">
      <a-card class="kpi-card gradient-1">
        <div class="kpi-content">
          <div class="kpi-icon"><DollarOutlined /></div>
          <div class="kpi-info">
            <div class="kpi-label">月度营收</div>
            <div class="kpi-value">¥{{ formatNumber(totalRevenue) }}</div>
            <div class="kpi-trend up"><ArrowUpOutlined /> 12.5%</div>
          </div>
        </div>
      </a-card>
      <a-card class="kpi-card gradient-2">
        <div class="kpi-content">
          <div class="kpi-icon"><ShoppingCartOutlined /></div>
          <div class="kpi-info">
            <div class="kpi-label">客单价</div>
            <div class="kpi-value">¥{{ avgCustomerPrice }}</div>
            <div class="kpi-trend up"><ArrowUpOutlined /> 5.2%</div>
          </div>
        </div>
      </a-card>
      <a-card class="kpi-card gradient-3">
        <div class="kpi-content">
          <div class="kpi-icon"><ReconciliationOutlined /></div>
          <div class="kpi-info">
            <div class="kpi-label">到店频次</div>
            <div class="kpi-value">{{ avgVisitFrequency }} 次/月</div>
            <div class="kpi-trend up"><ArrowUpOutlined /> 3.8%</div>
          </div>
        </div>
      </a-card>
      <a-card class="kpi-card gradient-4">
        <div class="kpi-content">
          <div class="kpi-icon"><UserAddOutlined /></div>
          <div class="kpi-info">
            <div class="kpi-label">新客数</div>
            <div class="kpi-value">{{ totalNewCustomers }} 人</div>
            <div class="kpi-trend down"><ArrowDownOutlined /> 2.1%</div>
          </div>
        </div>
      </a-card>
      <a-card class="kpi-card gradient-5">
        <div class="kpi-content">
          <div class="kpi-icon"><ReloadOutlined /></div>
          <div class="kpi-info">
            <div class="kpi-label">复购率</div>
            <div class="kpi-value">{{ (avgRepeatRate * 100).toFixed(1) }}%</div>
            <div class="kpi-trend up"><ArrowUpOutlined /> 4.6%</div>
          </div>
        </div>
      </a-card>
    </div>

    <div v-else class="compare-kpi-section">
      <div
        v-for="kpi in compareKpiList"
        :key="kpi.key"
        class="compare-kpi-card"
        :class="'gradient-' + kpi.gradient"
      >
        <div class="compare-kpi-header">
          <div class="kpi-icon-sm"><component :is="kpi.icon" /></div>
          <div class="compare-kpi-title">{{ kpi.label }}</div>
        </div>
        <div class="compare-kpi-rows">
          <div
            v-for="(store, idx) in getCompareStoreMetrics(kpi.key)"
            :key="store.storeId"
            class="compare-store-row"
          >
            <div class="store-left">
              <span
                class="store-dot"
                :style="{ backgroundColor: getStoreColor(store.storeId, idx) }"
              ></span>
              <span class="store-name">{{ store.storeName }}</span>
            </div>
            <div class="store-right">
              <span class="store-value">{{ kpi.formatter(Number(store[kpi.key]) || 0) }}</span>
              <span
                v-if="store.diff !== 0"
                class="store-diff"
                :class="store.diff > 0 ? 'diff-pos' : 'diff-neg'"
              >
                {{ store.diff > 0 ? '+' : '' }}{{ store.diff.toFixed(1) }}%
              </span>
              <span v-else class="store-diff diff-best">最佳</span>
            </div>
          </div>
        </div>
      </div>
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
          :row-class-name="getRowClassName"
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
            <template v-else-if="column.key === 'storeName'">
              <span class="rank-store-name">
                <a-tag
                  v-if="compareMode && compareStoreIds.includes(record.storeId)"
                  color="purple"
                  style="margin-right: 6px"
                >对比</a-tag>
                {{ record.storeName }}
              </span>
            </template>
            <template v-else-if="column.key === 'revenue'">¥{{ formatNumber(record.revenue) }}</template>
            <template v-else-if="column.key === 'customerPrice'">¥{{ record.customerPrice }}</template>
            <template v-else-if="column.key === 'visitFrequency'">{{ record.visitFrequency }} 次</template>
            <template v-else-if="column.key === 'repeatRate'">{{ (record.repeatRate * 100).toFixed(1) }}%</template>
          </template>
        </a-table>
      </a-card>

      <a-card class="trend-card">
        <template #title>
          <div class="trend-title">
            <span>{{ compareMode ? '门店对比趋势' : '营收趋势对比' }}</span>
            <a-select
              v-if="compareMode"
              v-model:value="trendMetric"
              size="small"
              style="width: 120px; margin-left: 12px"
            >
              <a-select-option value="revenue">营收</a-select-option>
              <a-select-option value="customerPrice">客单价</a-select-option>
              <a-select-option value="visitFrequency">到店频次</a-select-option>
              <a-select-option value="repeatRate">复购率</a-select-option>
            </a-select>
          </div>
        </template>
        <PlotlyChart
          :data="compareMode ? compareTrendChartData : trendChartData"
          :layout="compareMode ? compareTrendChartLayout : trendChartLayout"
          height="380px"
        />
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, h, defineComponent } from 'vue'
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

const compareMode = ref(false)
const compareModalOpen = ref(false)
const compareStoreIds = ref<string[]>([])
const confirmedCompareIds = ref<string[]>([])
const trendMetric = ref<'revenue' | 'customerPrice' | 'visitFrequency' | 'repeatRate'>('revenue')

const storeOptions = computed(() => {
  return metricsData.value.map(s => ({
    label: s.storeName,
    value: s.storeId,
  }))
})

const chartColors = ['#E8A0BF', '#6B5B95', '#F5C6A5', '#A7D8B0', '#B8C5E0']
const storeColorMap: Record<string, string> = {}
function getStoreColor(storeId: string, idx?: number): string {
  if (storeColorMap[storeId]) return storeColorMap[storeId]
  const order = idx ?? Object.keys(storeColorMap).length
  const c = chartColors[order % chartColors.length]
  storeColorMap[storeId] = c
  return c
}

function handleCompareModeChange(val: boolean) {
  if (val) {
    compareStoreIds.value = confirmedCompareIds.value.length > 0
      ? [...confirmedCompareIds.value]
      : metricsData.value.slice(0, Math.min(2, metricsData.value.length)).map(m => m.storeId)
    compareModalOpen.value = true
  } else {
    confirmedCompareIds.value = []
  }
}

function validateCompareSelection(val: string[]) {
  if (val.length > 3) {
    compareStoreIds.value = val.slice(0, 3)
  }
}

function confirmCompareStores() {
  if (compareStoreIds.value.length < 2) return
  confirmedCompareIds.value = [...compareStoreIds.value]
  compareStoreIds.value = [...confirmedCompareIds.value]
  compareModalOpen.value = false
}

function getRowClassName(record: StoreMetric) {
  return compareMode.value && confirmedCompareIds.value.includes(record.storeId)
    ? 'row-highlight'
    : ''
}

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

interface KpiDef {
  key: keyof StoreMetric
  label: string
  icon: ReturnType<typeof defineComponent>
  gradient: number
  higherIsBetter: boolean
  formatter: (v: number) => string
}
const KPI_GRAD_MAP = ['1', '2', '3', '4', '5']
const compareKpiList: KpiDef[] = [
  { key: 'revenue', label: '月度营收', icon: DollarOutlined, gradient: 1, higherIsBetter: true,
    formatter: (v: number) => '¥' + (v >= 10000 ? (v / 10000).toFixed(1) + '万' : v.toLocaleString()) },
  { key: 'customerPrice', label: '客单价', icon: ShoppingCartOutlined, gradient: 2, higherIsBetter: true,
    formatter: (v: number) => '¥' + Math.round(v).toLocaleString() },
  { key: 'visitFrequency', label: '到店频次', icon: ReconciliationOutlined, gradient: 3, higherIsBetter: true,
    formatter: (v: number) => (+v).toFixed(1) + ' 次/月' },
  { key: 'newCustomers', label: '新客数', icon: UserAddOutlined, gradient: 4, higherIsBetter: true,
    formatter: (v: number) => Math.round(v) + ' 人' },
  { key: 'repeatRate', label: '复购率', icon: ReloadOutlined, gradient: 5, higherIsBetter: true,
    formatter: (v: number) => (+v * 100).toFixed(1) + '%' },
]

function getCompareStoreMetrics(kpiKey: keyof StoreMetric) {
  const stores = metricsData.value.filter(m => confirmedCompareIds.value.includes(m.storeId))
  if (stores.length === 0) return []
  const vals = stores.map(s => Number(s[kpiKey]) || 0)
  const best = Math.max(...vals)
  return stores.map((s, idx) => {
    const v = Number(s[kpiKey]) || 0
    const diff = best === 0 ? 0 : ((v - best) / Math.abs(best)) * 100
    return {
      ...s,
      diff: +diff.toFixed(1),
    }
  })
}

const trendFieldMap: Record<string, string> = {
  revenue: 'revenue',
  customerPrice: 'customerPrice',
  visitFrequency: 'visitFrequency',
  newCustomers: 'newCustomers',
  repeatRate: 'repeatRate',
}

const trendYTitleMap: Record<string, string> = {
  revenue: '营收 (元)',
  customerPrice: '客单价 (元)',
  visitFrequency: '到店频次 (次/月)',
  newCustomers: '新客数 (人)',
  repeatRate: '复购率',
}

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
      line: { color: chartColors[idx % chartColors.length], width: 3, shape: 'spline' },
      marker: { size: 6, color: chartColors[idx % chartColors.length] },
      hovertemplate: '%{x}<br>营收: ¥%{y:,.0f}<extra></extra>',
    }
  })
})

const trendChartLayout = {
  margin: { l: 60, r: 30, t: 20, b: 40 },
  xaxis: { gridcolor: '#f0f0f0', zeroline: false },
  yaxis: {
    gridcolor: '#f0f0f0', zeroline: false, tickformat: ',.0f',
    title: { text: '营收 (元)', font: { size: 12, color: '#666' } },
  },
  legend: { orientation: 'h', y: -0.15, x: 0 },
  hovermode: 'x unified',
}

const compareTrendChartData = computed(() => {
  if (trendData.value.length === 0 || confirmedCompareIds.value.length === 0) return []
  const metric = trendMetric.value
  const field = trendFieldMap[metric]
  const stores = metricsData.value.filter(m => confirmedCompareIds.value.includes(m.storeId))
  return stores.map((store, idx) => {
    const color = getStoreColor(store.storeId, idx)
    const values = trendData.value.map(d => {
      const s = d.stores.find((x: any) => x.storeId === store.storeId)
      if (!s) return 0
      const raw = s[field] ?? 0
      return metric === 'repeatRate' ? +(raw * 100).toFixed(2) : raw
    })
    const hoverSuffix = metric === 'repeatRate' ? '%' : (metric === 'revenue' || metric === 'customerPrice' ? '元' : '')
    const hoverPrefix = metric === 'revenue' ? '¥' : ''
    return {
      x: trendData.value.map(d => d.date),
      y: values,
      type: 'scatter',
      mode: 'lines+markers',
      name: store.storeName,
      line: { color, width: 4, shape: 'spline' },
      marker: { size: 8, color },
      hovertemplate: `%{x}<br>${store.storeName}: ${hoverPrefix}%{y:,.0f}${hoverSuffix}<extra></extra>`,
    }
  })
})

const compareTrendChartLayout = computed(() => {
  const metric = trendMetric.value
  const yTitle = trendYTitleMap[metric]
  return {
    margin: { l: 60, r: 30, t: 20, b: 40 },
    xaxis: { gridcolor: '#f0f0f0', zeroline: false },
    yaxis: {
      gridcolor: '#f0f0f0', zeroline: false,
      tickformat: metric === 'repeatRate' ? ',.1f' : ',.0f',
      title: { text: yTitle, font: { size: 12, color: '#666' } },
    },
    legend: { orientation: 'h', y: -0.15, x: 0 },
    hovermode: 'x unified',
  }
})

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

function handleSortChange() {}

async function loadData() {
  try {
    const [metrics, trend] = await Promise.all([
      storeApi.getStoreMetrics(filterParams.value),
      storeApi.getStoreTrend(filterParams.value),
    ])
    metricsData.value = metrics
    trendData.value = trend
    if (metrics.length > 0 && confirmedCompareIds.value.length === 0 && !compareMode.value) {
      Object.keys(storeColorMap).forEach(k => delete storeColorMap[k])
    }
    if (metrics.length > 0 && confirmedCompareIds.value.length === 0) {
      confirmedCompareIds.value = metrics.slice(0, 2).map(m => m.storeId)
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

watch(
  () => filterParams.value,
  () => loadData(),
  { deep: true }
)

onMounted(() => loadData())
</script>

<style scoped>
.store-analysis {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.top-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: -8px;
}
.toolbar-right { display: flex; align-items: center; }
.mode-tag { font-size: 13px; font-weight: 500; }

.kpi-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.kpi-card {
  border: none !important;
  overflow: hidden;
}
.kpi-card :deep(.ant-card-body) { padding: 20px !important; }

.gradient-1 { background: linear-gradient(135deg, #FCE7F3 0%, #FBCFE8 100%); }
.gradient-2 { background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%); }
.gradient-3 { background: linear-gradient(135deg, #FFF0E6 0%, #FFE4D1 100%); }
.gradient-4 { background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); }
.gradient-5 { background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); }

.kpi-content { display: flex; align-items: center; gap: 16px; }
.kpi-icon {
  width: 52px; height: 52px; border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; color: #6B5B95;
}
.kpi-info { flex: 1; }
.kpi-label { font-size: 13px; color: #666; margin-bottom: 4px; }
.kpi-value { font-size: 24px; font-weight: 700; color: #333; margin-bottom: 4px; }
.kpi-trend { font-size: 12px; display: flex; align-items: center; gap: 2px; }
.kpi-trend.up { color: #52c41a; }
.kpi-trend.down { color: #ff4d4f; }

.compare-kpi-section {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}
.compare-kpi-card {
  border-radius: 12px;
  padding: 18px 20px;
  border: none !important;
  min-height: 240px;
}
.compare-kpi-card :deep(.ant-card-body) { padding: 0 !important; }
.compare-kpi-header {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}
.kpi-icon-sm {
  width: 40px; height: 40px; border-radius: 10px;
  background: rgba(255, 255, 255, 0.7);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; color: #6B5B95;
}
.compare-kpi-title {
  font-size: 14px; font-weight: 600; color: #333;
}
.compare-kpi-rows {
  display: flex; flex-direction: column; gap: 10px;
}
.compare-store-row {
  display: flex; justify-content: space-between; align-items: center;
  background: rgba(255, 255, 255, 0.45);
  border-radius: 8px;
  padding: 10px 12px;
}
.store-left { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0; }
.store-dot {
  width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.6);
}
.store-name {
  font-size: 13px; color: #333; font-weight: 500;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.store-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.store-value { font-size: 15px; font-weight: 700; color: #222; }
.store-diff { font-size: 12px; font-weight: 600; }
.store-diff.diff-pos { color: #52c41a; }
.store-diff.diff-neg { color: #ff4d4f; }
.store-diff.diff-best { color: #1677ff; }

.trend-title { display: flex; align-items: center; }

.rank-store-name { display: inline-flex; align-items: center; }

:deep(.row-highlight > td) {
  background-color: rgba(137, 89, 221, 0.06) !important;
}
:deep(.row-highlight > td:first-child) {
  border-left: 3px solid #8959dd;
}

.chart-section {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
}
.ranking-card, .trend-card { min-height: 420px; }

@media (max-width: 1200px) {
  .kpi-cards, .compare-kpi-section { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 900px) {
  .kpi-cards, .compare-kpi-section { grid-template-columns: repeat(2, 1fr); }
  .chart-section { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
  .kpi-cards, .compare-kpi-section { grid-template-columns: 1fr; }
}
</style>
