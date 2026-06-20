<template>
  <div class="employee-analysis">
    <div class="filter-row">
      <div class="filter-item">
        <span class="filter-label">服务类型</span>
        <a-select
          v-model:value="serviceType"
          style="width: 160px"
          @change="handleServiceTypeChange"
        >
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="皮肤管理">皮肤管理</a-select-option>
          <a-select-option value="抗衰紧致">抗衰紧致</a-select-option>
          <a-select-option value="美甲美睫">美甲美睫</a-select-option>
          <a-select-option value="脱毛">脱毛</a-select-option>
          <a-select-option value="纹绣">纹绣</a-select-option>
        </a-select>
      </div>
    </div>

    <div class="top-section">
      <a-card title="业绩排行榜" class="ranking-card">
        <a-table
          :columns="rankingColumns"
          :data-source="rankingData"
          :pagination="false"
          size="middle"
          row-key="empId"
          :custom-row="handleRowClick"
        >
          <template #bodyCell="{ column, record, index }">
            <template v-if="column.key === 'rank'">
              <span
                class="rank-badge"
                :class="{
                'rank-1': index === 0,
                'rank-2': index === 1,
                'rank-3': index === 2,
              }"
              >
                {{ index + 1 }}
              </span>
            </template>
            <template v-else-if="column.key === 'empName'">
              <div class="employee-info">
                <a-avatar
                :style="{ backgroundColor: getAvatarColor(index) }"
                size="small"
              >
                {{ record.empName.charAt(0) }}
              </a-avatar>
              <span>{{ record.empName }}</span>
            </div>
            </template>
            <template v-else-if="column.key === 'cardAmount'">
              <span class="amount-text">¥{{ formatNumber(record.cardAmount) }}</span>
            </template>
            <template v-else-if="column.key === 'avgPrice'">
              ¥{{ record.avgPrice }}
            </template>
            <template v-else-if="column.key === 'action'">
              <a-button type="link" size="small" @click.stop="openDetail(record)">
                <LineChartOutlined /> 趋势
              </a-button>
            </template>
          </template>
        </a-table>
      </a-card>

      <a-card title="员工业绩分布" class="bar-card">
        <PlotlyChart
          :data="barChartData"
          :layout="barChartLayout"
          height="380px"
        />
      </a-card>
    </div>

    <a-card title="客单数与客单价对比" class="compare-card">
      <PlotlyChart
        :data="compareChartData"
        :layout="compareChartLayout"
        height="380px"
      />
    </a-card>

    <a-drawer
      v-model:open="detailDrawerOpen"
      :title="currentEmployee?.empName + ' - 业绩走势'"
      width="720px"
      :mask-closable="false"
      @close="closeDetail"
    >
      <div v-if="trendData.employee" class="employee-detail">
        <div class="emp-info-card">
          <a-avatar
            :style="{ backgroundColor: '#E8A0BF' }"
            size="large"
          >
            {{ currentEmployee?.empName?.charAt(0) }}
          </a-avatar>
          <div class="emp-info">
            <div class="emp-name">{{ trendData.employee.empName }}</div>
            <div class="emp-meta">
              <span>{{ trendData.employee.position }}</span>
              <span class="dot">·</span>
              <span>{{ trendData.employee.serviceType }}</span>
              <span class="dot">·</span>
              <span>{{ trendData.employee.storeName }}</span>
            </div>
          </div>
          <div class="emp-months-selector">
            <span class="selector-label">查看最近</span>
            <a-select
              v-model:value="trendMonths"
              style="width: 90px"
              size="small"
              @change="loadTrendData"
            >
              <a-select-option :value="3">3 个月</a-select-option>
              <a-select-option :value="6">6 个月</a-select-option>
              <a-select-option :value="9">9 个月</a-select-option>
              <a-select-option :value="12">12 个月</a-select-option>
            </a-select>
          </div>
        </div>

        <div class="summary-stats">
          <div class="stat-item">
            <div class="stat-label">累计划卡</div>
            <div class="stat-value">¥{{ formatNumber(totalCardAmount) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">累计客单</div>
            <div class="stat-value">{{ totalOrderCount }} 单</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">平均客单价</div>
            <div class="stat-value">¥{{ avgPriceAll.toFixed(0) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">业绩趋势</div>
            <div class="stat-value">
              <a-tag :color="trendDirectionColor">
                <component :is="trendDirectionIcon" />
                {{ trendDirectionText }}
              </a-tag>
            </div>
          </div>
        </div>

        <a-card title="划卡总额与客单数趋势" class="trend-card">
          <PlotlyChart
            :data="trendChartData"
            :layout="trendChartLayout"
            height="360px"
          />
        </a-card>
      </div>
      <a-spin v-else :spinning="loadingTrend" tip="加载中...">
        <div style="min-height: 200px"></div>
      </a-spin>
    </a-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Avatar } from 'ant-design-vue'
import {
  LineChartOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  MinusOutlined,
} from '@ant-design/icons-vue'
import PlotlyChart from '@/components/charts/PlotlyChart.vue'
import { employeeApi } from '@/api/employee'
import { useFilter } from '@/composables/useFilter'
import type { EmployeeRanking, EmployeeOrderData, EmployeeTrendResponse, EmployeeTrendItem } from '@/types'

const { filterParams } = useFilter()

const serviceType = ref('all')
const rankingData = ref<EmployeeRanking[]>([])
const orderData = ref<EmployeeOrderData[]>([])

const detailDrawerOpen = ref(false)
const currentEmployee = ref<EmployeeRanking | null>(null)
const trendMonths = ref(6)
const loadingTrend = ref(false)
const trendData = ref<EmployeeTrendResponse>({ employee: null, trend: [] })

const chartColors = [
  '#E8A0BF',
  '#6B5B95',
  '#F5C6A5',
  '#A7D8B0',
  '#B8C5E0',
  '#FFD700',
  '#87CEEB',
  '#FFA07A',
]

const avatarColors = ['#E8A0BF', '#6B5B95', '#F5C6A5', '#A7D8B0', '#B8C5E0']

const rankingColumns = [
  { title: '排名', key: 'rank', width: 70, align: 'center' },
  { title: '姓名', key: 'empName', dataIndex: 'empName' },
  { title: '门店', dataIndex: 'storeName', key: 'storeName' },
  { title: '服务类型', dataIndex: 'serviceType', key: 'serviceType' },
  { title: '划卡总额', dataIndex: 'cardAmount', key: 'cardAmount' },
  { title: '客单数', dataIndex: 'orderCount', key: 'orderCount' },
  { title: '客单价', dataIndex: 'avgPrice', key: 'avgPrice' },
  {
    title: '操作',
    key: 'action',
    width: 100,
    align: 'center',
  },
]

const barChartData = computed(() => {
  const sorted = [...rankingData.value].sort((a, b) => b.cardAmount - a.cardAmount)
  return [
    {
      x: sorted.map(d => d.cardAmount),
      y: sorted.map(d => d.empName),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: sorted.map((_, i) => chartColors[i % chartColors.length]),
        borderRadius: [0, 6, 6, 0],
      },
      text: sorted.map(d => `¥${formatNumber(d.cardAmount)}`),
      textposition: 'auto',
      hovertemplate:
        '<b>%{y}</b><br>划卡总额: ¥%{x:,.0f}<extra></extra>',
    },
  ]
})

const barChartLayout = {
  margin: { l: 80, r: 40, t: 20, b: 40 },
  xaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    title: {
      text: '划卡总额 (元)',
      font: { size: 12, color: '#666' },
    },
    tickformat: ',.0f',
  },
  yaxis: {
    showgrid: false,
    zeroline: false,
    autorange: 'reversed',
  },
  showlegend: false,
}

const compareChartData = computed(() => {
  const data = orderData.value
  return [
    {
      x: data.map(d => d.empName),
      y: data.map(d => d.orderCount),
      type: 'bar',
      name: '客单数',
      yaxis: 'y',
      marker: {
        color: '#E8A0BF',
        borderRadius: [6, 6, 0, 0],
      },
      hovertemplate: '<b>%{x}</b><br>客单数: %{y}<extra></extra>',
    },
    {
      x: data.map(d => d.empName),
      y: data.map(d => d.avgPrice),
      type: 'scatter',
      mode: 'lines+markers',
      name: '客单价',
      yaxis: 'y2',
      line: {
        color: '#6B5B95',
        width: 3,
        shape: 'spline',
      },
      marker: {
        size: 8,
        color: '#6B5B95',
      },
      hovertemplate: '<b>%{x}</b><br>客单价: ¥%{y}<extra></extra>',
    },
  ]
})

const compareChartLayout = {
  margin: { l: 60, r: 60, t: 20, b: 40 },
  xaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
  },
  yaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    title: {
      text: '客单数',
      font: { size: 12, color: '#E8A0BF' },
    },
  },
  yaxis2: {
    overlaying: 'y',
    side: 'right',
    showgrid: false,
    zeroline: false,
    title: {
      text: '客单价 (元)',
      font: { size: 12, color: '#6B5B95' },
    },
  },
  legend: {
    orientation: 'h',
    y: -0.15,
    x: 0,
  },
}

const totalCardAmount = computed(() => {
  return trendData.value.trend.reduce((sum, item) => sum + item.cardAmount, 0)
})

const totalOrderCount = computed(() => {
  return trendData.value.trend.reduce((sum, item) => sum + item.orderCount, 0)
})

const avgPriceAll = computed(() => {
  return totalOrderCount.value > 0 ? totalCardAmount.value / totalOrderCount.value : 0
})

const trendDirection = computed(() => {
  const trend = trendData.value.trend
  if (trend.length < 2) return 0
  const first = trend[0].cardAmount
  const last = trend[trend.length - 1].cardAmount
  if (first === 0) return 0
  const change = ((last - first) / Math.abs(first)) * 100
  return change
})

const trendDirectionIcon = computed(() => {
  if (trendDirection.value > 1) return ArrowUpOutlined
  if (trendDirection.value < -1) return ArrowDownOutlined
  return MinusOutlined
})

const trendDirectionColor = computed(() => {
  if (trendDirection.value > 1) return 'green'
  if (trendDirection.value < -1) return 'red'
  return 'default'
})

const trendDirectionText = computed(() => {
  if (trendDirection.value > 1) return `上升 ${trendDirection.value.toFixed(1)}%`
  if (trendDirection.value < -1) return `下降 ${Math.abs(trendDirection.value).toFixed(1)}%`
  return '持平'
})

const trendChartData = computed(() => {
  const data = trendData.value.trend
  if (data.length === 0) return []
  return [
    {
      x: data.map(d => d.statMonth),
      y: data.map(d => d.cardAmount),
      type: 'scatter',
      mode: 'lines+markers',
      name: '划卡总额',
      yaxis: 'y',
      line: {
        color: '#E8A0BF',
        width: 3,
        shape: 'spline',
      },
      marker: {
        size: 8,
        color: '#E8A0BF',
      },
      hovertemplate: '<b>%{x}</b><br>划卡总额: ¥%{y:,.0f}<extra></extra>',
    },
    {
      x: data.map(d => d.statMonth),
      y: data.map(d => d.orderCount),
      type: 'scatter',
      mode: 'lines+markers',
      name: '客单数',
      yaxis: 'y2',
      line: {
        color: '#6B5B95',
        width: 3,
        shape: 'spline',
        dash: 'dash',
      },
      marker: {
        size: 8,
        color: '#6B5B95',
        symbol: 'diamond',
      },
      hovertemplate: '<b>%{x}</b><br>客单数: %{y}<extra></extra>',
    },
  ]
})

const trendChartLayout = computed(() => ({
  margin: { l: 70, r: 70, t: 20, b: 40 },
  xaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
  },
  yaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    title: {
      text: '划卡总额 (元)',
      font: { size: 12, color: '#E8A0BF' },
    },
    tickformat: ',.0f',
  },
  yaxis2: {
    overlaying: 'y',
    side: 'right',
    showgrid: false,
    zeroline: false,
    title: {
      text: '客单数',
      font: { size: 12, color: '#6B5B95' },
    },
  },
  legend: {
    orientation: 'h',
    y: -0.15,
    x: 0,
  },
}))

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

function getAvatarColor(index: number): string {
  return avatarColors[index % avatarColors.length]
}

function handleServiceTypeChange() {
  loadData()
}

function handleRowClick(record: EmployeeRanking) {
  return {
    style: { cursor: 'pointer' },
    onClick: () => openDetail(record),
  }
}

function openDetail(record: EmployeeRanking) {
  currentEmployee.value = record
  detailDrawerOpen.value = true
  trendData.value = { employee: null, trend: [] }
  loadTrendData()
}

function closeDetail() {
  detailDrawerOpen.value = false
  currentEmployee.value = null
  trendData.value = { employee: null, trend: [] }
}

async function loadTrendData() {
  if (!currentEmployee.value) return
  loadingTrend.value = true
  try {
    const endDate = filterParams.value.endDate
    const data = await employeeApi.getEmployeeTrend(
      currentEmployee.value.empId,
      trendMonths.value,
      endDate
    )
    trendData.value = data
  } catch (error) {
    console.error('加载员工业绩趋势失败:', error)
  } finally {
    loadingTrend.value = false
  }
}

async function loadData() {
  try {
    const params = {
      ...filterParams.value,
      serviceType: serviceType.value,
    }
    const [ranking, orders] = await Promise.all([
      employeeApi.getEmployeeRanking(params),
      employeeApi.getEmployeeOrders(params),
    ])
    rankingData.value = ranking
    orderData.value = orders
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
.employee-analysis {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666;
}

.top-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.ranking-card,
.bar-card {
  min-height: 440px;
}

.compare-card {
  min-height: 440px;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f0f0;
  color: #999;
  font-weight: 600;
  font-size: 13px;
}

.rank-badge.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #fff;
}

.rank-badge.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A8A8A8);
  color: #fff;
}

.rank-badge.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #B87333);
  color: #fff;
}

.employee-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.amount-text {
  color: #E8A0BF;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .top-section {
    grid-template-columns: 1fr;
  }
}

.employee-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.emp-info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #fef6fa 0%, #f5f0ff 100%);
  border-radius: 12px;
}

.emp-info {
  flex: 1;
}

.emp-name {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.emp-meta {
  font-size: 13px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
}

.emp-meta .dot {
  color: #ccc;
}

.emp-months-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.selector-label {
  font-size: 13px;
  color: #666;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-item {
  background: #fafafa;
  padding: 16px;
  border-radius: 10px;
  text-align: center;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.trend-card {
  min-height: 420px;
}

@media (max-width: 768px) {
  .summary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
