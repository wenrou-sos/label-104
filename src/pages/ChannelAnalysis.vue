<template>
  <div class="channel-analysis">
    <div class="top-section">
      <a-card title="渠道转化率对比" class="conversion-card">
        <PlotlyChart
          :data="conversionChartData"
          :layout="conversionChartLayout"
          height="380px"
        />
      </a-card>

      <a-card title="渠道客单价对比" class="aov-card">
        <PlotlyChart
          :data="aovChartData"
          :layout="aovChartLayout"
          height="380px"
        />
      </a-card>
    </div>

    <a-card class="roi-summary-card">
      <template #title>
        <span>投放 ROI 总览</span>
      </template>
      <template #extra>
        <a-button type="primary" @click="openCostDrawer">
          <template #icon><EditOutlined /></template>
          成本录入
        </a-button>
      </template>
      <div class="roi-summary-grid">
        <div class="summary-item">
          <div class="summary-label">总投放成本</div>
          <div class="summary-value cost">¥{{ formatNumber(totalCost) }}</div>
        </div>
        <div class="summary-item">
          <div class="summary-label">总营收</div>
          <div class="summary-value revenue">¥{{ formatNumber(totalRevenue) }}</div>
        </div>
        <div class="summary-item">
          <div class="summary-label">总利润</div>
          <div class="summary-value profit" :class="{ negative: totalProfit < 0 }">
            ¥{{ formatNumber(totalProfit) }}
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-label">整体 ROI</div>
          <div class="summary-value roi" :class="{ negative: overallRoi < 0 }">
            {{ overallRoi !== null ? overallRoi.toFixed(1) + '%' : '--' }}
          </div>
        </div>
      </div>
    </a-card>

    <a-card title="渠道 ROI 评估排名" class="evaluation-card">
      <a-table
        :columns="evaluationColumns"
        :data-source="sortedEvaluationData"
        :pagination="false"
        size="middle"
        row-key="channelId"
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
          <template v-else-if="column.key === 'channelName'">
            <div class="channel-info">
              <div
                class="channel-icon"
                :style="{ backgroundColor: getChannelColor(record.channelId) }"
              >
                {{ record.channelName.charAt(0) }}
              </div>
              <span>{{ record.channelName }}</span>
            </div>
          </template>
          <template v-else-if="column.key === 'roi'">
            <span class="roi-value" :class="getRoiClass(record.roiLevel)">
              {{ record.roi !== null ? record.roi.toFixed(1) + '%' : '--' }}
            </span>
          </template>
          <template v-else-if="column.key === 'totalCost' || column.key === 'totalRevenue' || column.key === 'profit'">
            <span :class="{ 'negative-value': column.key === 'profit' && record.profit < 0 }">
              ¥{{ formatNumber(record[column.key]) }}
            </span>
          </template>
          <template v-else-if="column.key === 'totalScore'">
            <a-progress
              :percent="record.totalScore"
              :stroke-color="getScoreColor(record.totalScore)"
              size="small"
            />
          </template>
          <template v-else-if="column.key === 'suggestion'">
            <a-tooltip :title="record.suggestion">
              <span class="suggestion-text">{{ record.suggestion }}</span>
            </a-tooltip>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-drawer
      v-model:open="costDrawerVisible"
      title="渠道月度成本录入"
      width="720px"
      :mask-closable="false"
      @close="handleCostDrawerClose"
    >
      <div class="cost-drawer-content">
        <div class="cost-filter-bar">
          <a-select v-model:value="selectedMonth" style="width: 160px">
            <a-select-option v-for="m in availableMonths" :key="m" :value="m">
              {{ m }}
            </a-select-option>
          </a-select>
          <span class="cost-filter-tip">选择月份，录入各渠道当月投放成本</span>
        </div>

        <a-table
          :columns="costTableColumns"
          :data-source="costTableData"
          :pagination="false"
          size="middle"
          row-key="channelId"
          bordered
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'channelName'">
              <div class="channel-info">
                <div
                  class="channel-icon small"
                  :style="{ backgroundColor: getChannelColor(record.channelId) }"
                >
                  {{ record.channelName.charAt(0) }}
                </div>
                <span>{{ record.channelName }}</span>
              </div>
            </template>
            <template v-else-if="column.key === 'cost'">
              <a-input-number
                v-model:value="editingCosts[record.channelId]"
                :min="0"
                :precision="2"
                style="width: 100%"
                placeholder="输入投放成本"
                @change="handleCostChange(record.channelId, $event)"
              />
            </template>
          </template>
        </a-table>

        <div class="cost-drawer-footer">
          <a-button @click="handleCostDrawerClose">取消</a-button>
          <a-button type="primary" @click="saveCosts" :loading="savingCosts">
            保存成本
          </a-button>
        </div>
      </div>
    </a-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, reactive } from 'vue'
import { EditOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import PlotlyChart from '@/components/charts/PlotlyChart.vue'
import { channelApi } from '@/api/channel'
import { channelCostApi } from '@/api/channelCost'
import { useFilter } from '@/composables/useFilter'
import type {
  ChannelConversion,
  ChannelAov,
  ChannelEvaluation,
  ChannelCostMap,
} from '@/types'

const { filterParams } = useFilter()

const conversionData = ref<ChannelConversion[]>([])
const aovData = ref<ChannelAov[]>([])
const evaluationData = ref<ChannelEvaluation[]>([])
const allCosts = ref<ChannelCostMap>({})

const costDrawerVisible = ref(false)
const selectedMonth = ref('')
const editingCosts = reactive<Record<string, number>>({})
const savingCosts = ref(false)

const chartColors = {
  C001: '#E8A0BF',
  C002: '#6B5B95',
  C003: '#F5C6A5',
  C004: '#A7D8B0',
  C005: '#B8C5E0',
  C006: '#FFD700',
}

const costTableColumns = [
  { title: '渠道名称', key: 'channelName', dataIndex: 'channelName', width: 200 },
  { title: '渠道类型', dataIndex: 'channelType', key: 'channelType', width: 140 },
  { title: '月度投放成本（元）', key: 'cost', dataIndex: 'cost' },
]

const evaluationColumns = [
  { title: '排名', key: 'rank', width: 70, align: 'center' as const },
  { title: '渠道名称', key: 'channelName', dataIndex: 'channelName', width: 160 },
  { title: '投放成本', dataIndex: 'totalCost', key: 'totalCost', width: 120, align: 'right' as const },
  { title: '总营收', dataIndex: 'totalRevenue', key: 'totalRevenue', width: 120, align: 'right' as const },
  { title: '净利润', dataIndex: 'profit', key: 'profit', width: 120, align: 'right' as const },
  { title: 'ROI', dataIndex: 'roi', key: 'roi', width: 100, align: 'right' as const, sorter: (a: ChannelEvaluation, b: ChannelEvaluation) => (a.roi ?? -999) - (b.roi ?? -999) },
  { title: '综合评分', key: 'totalScore', dataIndex: 'totalScore', width: 160 },
  { title: '优化建议', key: 'suggestion', dataIndex: 'suggestion', width: 240 },
]

const sortedEvaluationData = computed(() => {
  return [...evaluationData.value].sort((a, b) => {
    const roiA = a.roi ?? -Infinity
    const roiB = b.roi ?? -Infinity
    return roiB - roiA
  })
})

const totalCost = computed(() => {
  return evaluationData.value.reduce((sum, item) => sum + (item.totalCost || 0), 0)
})

const totalRevenue = computed(() => {
  return evaluationData.value.reduce((sum, item) => sum + (item.totalRevenue || 0), 0)
})

const totalProfit = computed(() => {
  return evaluationData.value.reduce((sum, item) => sum + (item.profit || 0), 0)
})

const overallRoi = computed(() => {
  if (totalCost.value > 0) {
    return ((totalRevenue.value - totalCost.value) / totalCost.value) * 100
  }
  return null
})

const availableMonths = computed(() => {
  const months: string[] = []
  for (let m = 1; m <= 12; m++) {
    months.push(`2024-${String(m).padStart(2, '0')}`)
  }
  return months.reverse()
})

const costTableData = computed(() => {
  return evaluationData.value.map(item => ({
    channelId: item.channelId,
    channelName: item.channelName,
    channelType: item.channelType,
    cost: allCosts.value[item.channelId]?.[selectedMonth.value] || 0,
  }))
})

const conversionChartData = computed(() => {
  const sorted = [...conversionData.value].sort(
    (a, b) => b.conversionRate - a.conversionRate
  )
  return [
    {
      x: sorted.map(d => d.channelName),
      y: sorted.map(d => d.conversionRate * 100),
      type: 'bar',
      name: '转化率',
      marker: {
        color: sorted.map(d => chartColors[d.channelId as keyof typeof chartColors] || '#E8A0BF'),
        borderRadius: [6, 6, 0, 0],
      },
      text: sorted.map(d => (d.conversionRate * 100).toFixed(1) + '%'),
      textposition: 'outside',
      hovertemplate:
        '<b>%{x}</b><br>曝光: %{customdata[0]:,}<br>点击: %{customdata[1]:,}<br>到店: %{customdata[2]}人<br>转化率: %{y:.1f}%<extra></extra>',
      customdata: sorted.map(d => [
        d.exposureCount,
        d.clickCount,
        d.arrivalCount,
      ]),
    },
  ]
})

const conversionChartLayout = {
  margin: { l: 60, r: 30, t: 20, b: 40 },
  xaxis: {
    showgrid: false,
    zeroline: false,
  },
  yaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    title: {
      text: '转化率 (%)',
      font: { size: 12, color: '#666' },
    },
    tickformat: '.1f',
  },
  showlegend: false,
}

const aovChartData = computed(() => {
  const sorted = [...aovData.value].sort((a, b) => b.avgPrice - a.avgPrice)
  return [
    {
      x: sorted.map(d => d.channelName),
      y: sorted.map(d => d.avgPrice),
      type: 'bar',
      name: '客单价',
      marker: {
        color: sorted.map(d => chartColors[d.channelId as keyof typeof chartColors] || '#6B5B95'),
        borderRadius: [6, 6, 0, 0],
      },
      text: sorted.map(d => '¥' + d.avgPrice),
      textposition: 'outside',
      hovertemplate:
        '<b>%{x}</b><br>客单价: ¥%{y}<br>总营收: ¥%{customdata[0]:,}<br>客户数: %{customdata[1]}人<extra></extra>',
      customdata: sorted.map(d => [d.totalRevenue, d.customerCount]),
    },
  ]
})

const aovChartLayout = {
  margin: { l: 60, r: 30, t: 20, b: 40 },
  xaxis: {
    showgrid: false,
    zeroline: false,
  },
  yaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    title: {
      text: '客单价 (元)',
      font: { size: 12, color: '#666' },
    },
  },
  showlegend: false,
}

function getChannelColor(channelId: string): string {
  return chartColors[channelId as keyof typeof chartColors] || '#E8A0BF'
}

function getScoreColor(score: number): string {
  if (score >= 85) return '#52c41a'
  if (score >= 70) return '#1890ff'
  if (score >= 60) return '#faad14'
  return '#ff4d4f'
}

function getRoiClass(level: string): string {
  const map: Record<string, string> = {
    excellent: 'roi-excellent',
    good: 'roi-good',
    medium: 'roi-medium',
    low: 'roi-low',
    negative: 'roi-negative',
    unknown: 'roi-unknown',
  }
  return map[level] || 'roi-unknown'
}

function formatNumber(num: number): string {
  if (num === null || num === undefined) return '0'
  return num.toLocaleString('zh-CN', { maximumFractionDigits: 0 })
}

function openCostDrawer() {
  if (evaluationData.value.length > 0 && availableMonths.value.length > 0) {
    selectedMonth.value = availableMonths.value[0]
  }
  costDrawerVisible.value = true
  syncEditingCosts()
}

function syncEditingCosts() {
  evaluationData.value.forEach(item => {
    const monthCost = allCosts.value[item.channelId]?.[selectedMonth.value]
    editingCosts[item.channelId] = monthCost ?? 0
  })
}

function handleCostChange(channelId: string, value: number | null) {
  editingCosts[channelId] = value ?? 0
}

function handleCostDrawerClose() {
  costDrawerVisible.value = false
}

async function saveCosts() {
  savingCosts.value = true
  try {
    const costsData = Object.entries(editingCosts).map(([channelId, cost]) => ({
      channelId,
      statMonth: selectedMonth.value,
      cost: cost || 0,
    }))

    await channelCostApi.batchSaveChannelCosts(costsData)

    allCosts.value = await channelCostApi.getAllChannelCosts()
    await loadEvaluation()

    message.success('成本保存成功')
    costDrawerVisible.value = false
  } catch (error) {
    console.error('保存成本失败:', error)
    message.error('保存失败，请重试')
  } finally {
    savingCosts.value = false
  }
}

async function loadData() {
  try {
    const [conversion, aov, costs] = await Promise.all([
      channelApi.getChannelConversion(filterParams.value),
      channelApi.getChannelAov(filterParams.value),
      channelCostApi.getAllChannelCosts(),
    ])
    conversionData.value = conversion
    aovData.value = aov
    allCosts.value = costs as ChannelCostMap
    await loadEvaluation()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

async function loadEvaluation() {
  try {
    const evaluation = await channelApi.getChannelEvaluation(filterParams.value)
    evaluationData.value = evaluation
  } catch (error) {
    console.error('加载评估数据失败:', error)
  }
}

watch(
  () => filterParams.value,
  () => {
    loadData()
  },
  { deep: true }
)

watch(selectedMonth, () => {
  if (costDrawerVisible.value) {
    syncEditingCosts()
  }
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.channel-analysis {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.top-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.conversion-card,
.aov-card {
  min-height: 440px;
}

.roi-summary-card {
  min-height: 140px;
}

.roi-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.summary-item {
  text-align: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
}

.summary-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.summary-value {
  font-size: 26px;
  font-weight: 700;
}

.summary-value.cost {
  color: #fa8c16;
}

.summary-value.revenue {
  color: #1890ff;
}

.summary-value.profit {
  color: #52c41a;
}

.summary-value.profit.negative {
  color: #ff4d4f;
}

.summary-value.roi {
  color: #722ed1;
}

.summary-value.roi.negative {
  color: #ff4d4f;
}

.evaluation-card {
  min-height: 400px;
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

.channel-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.channel-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}

.channel-icon.small {
  width: 28px;
  height: 28px;
  font-size: 12px;
  border-radius: 6px;
}

.suggestion-text {
  font-size: 13px;
  color: #666;
}

.roi-value {
  font-weight: 600;
  font-size: 14px;
}

.roi-excellent {
  color: #52c41a;
}

.roi-good {
  color: #1890ff;
}

.roi-medium {
  color: #faad14;
}

.roi-low {
  color: #fa8c16;
}

.roi-negative {
  color: #ff4d4f;
}

.roi-unknown {
  color: #999;
}

.negative-value {
  color: #ff4d4f;
}

.cost-drawer-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cost-filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cost-filter-tip {
  font-size: 12px;
  color: #999;
}

.cost-drawer-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

@media (max-width: 900px) {
  .top-section {
    grid-template-columns: 1fr;
  }

  .roi-summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
