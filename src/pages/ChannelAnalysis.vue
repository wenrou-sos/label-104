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

    <a-card title="渠道效果综合评估" class="evaluation-card">
      <a-table
        :columns="evaluationColumns"
        :data-source="evaluationData"
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import PlotlyChart from '@/components/charts/PlotlyChart.vue'
import { channelApi } from '@/api/channel'
import { useFilter } from '@/composables/useFilter'
import type {
  ChannelConversion,
  ChannelAov,
  ChannelEvaluation,
} from '@/types'

const { filterParams } = useFilter()

const conversionData = ref<ChannelConversion[]>([])
const aovData = ref<ChannelAov[]>([])
const evaluationData = ref<ChannelEvaluation[]>([])

const chartColors = {
  C001: '#E8A0BF',
  C002: '#6B5B95',
  C003: '#F5C6A5',
  C004: '#A7D8B0',
  C005: '#B8C5E0',
  C006: '#FFD700',
}

const evaluationColumns = [
  { title: '排名', key: 'rank', width: 70, align: 'center' },
  { title: '渠道名称', key: 'channelName', dataIndex: 'channelName', width: 150 },
  { title: '转化得分', dataIndex: 'conversionScore', key: 'conversionScore', width: 100 },
  { title: '营收得分', dataIndex: 'revenueScore', key: 'revenueScore', width: 100 },
  { title: '成本得分', dataIndex: 'costScore', key: 'costScore', width: 100 },
  { title: '综合评分', key: 'totalScore', dataIndex: 'totalScore', width: 180 },
  { title: '优化建议', key: 'suggestion', dataIndex: 'suggestion' },
]

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

async function loadData() {
  try {
    const [conversion, aov, evaluation] = await Promise.all([
      channelApi.getChannelConversion(filterParams.value),
      channelApi.getChannelAov(filterParams.value),
      channelApi.getChannelEvaluation(filterParams.value),
    ])
    conversionData.value = conversion
    aovData.value = aov
    evaluationData.value = [...evaluation].sort((a, b) => b.totalScore - a.totalScore)
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

.suggestion-text {
  font-size: 13px;
  color: #666;
}

@media (max-width: 900px) {
  .top-section {
    grid-template-columns: 1fr;
  }
}
</style>
