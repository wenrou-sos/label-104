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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Avatar } from 'ant-design-vue'
import PlotlyChart from '@/components/charts/PlotlyChart.vue'
import { employeeApi } from '@/api/employee'
import { useFilter } from '@/composables/useFilter'
import type { EmployeeRanking, EmployeeOrderData } from '@/types'

const { filterParams } = useFilter()

const serviceType = ref('all')
const rankingData = ref<EmployeeRanking[]>([])
const orderData = ref<EmployeeOrderData[]>([])

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
</style>
