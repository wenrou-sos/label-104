<template>
  <div class="member-lifecycle">
    <div class="kpi-cards">
      <a-card class="kpi-card gradient-1">
        <div class="kpi-content">
          <div class="kpi-icon">
            <CalendarOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">平均充值周期</div>
            <div class="kpi-value">{{ cycleStats.avgRechargeCycle }} 天</div>
            <div class="kpi-trend up">
              <ArrowUpOutlined /> 较上月缩短3天
            </div>
          </div>
        </div>
      </a-card>

      <a-card class="kpi-card gradient-2">
        <div class="kpi-content">
          <div class="kpi-icon">
            <ReloadOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">90天复充率</div>
            <div class="kpi-value">{{ (cycleStats.rechargeRate * 100).toFixed(1) }}%</div>
            <div class="kpi-trend up">
              <ArrowUpOutlined /> 2.5%
            </div>
          </div>
        </div>
      </a-card>

      <a-card class="kpi-card gradient-3">
        <div class="kpi-content">
          <div class="kpi-icon">
            <TeamOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">会员总数</div>
            <div class="kpi-value">{{ formatNumber(cycleStats.totalMembers) }} 人</div>
            <div class="kpi-trend up">
              <ArrowUpOutlined /> 5.2%
            </div>
          </div>
        </div>
      </a-card>

      <a-card class="kpi-card gradient-4">
        <div class="kpi-content">
          <div class="kpi-icon">
            <UserOutlined />
          </div>
          <div class="kpi-info">
            <div class="kpi-label">活跃会员</div>
            <div class="kpi-value">{{ formatNumber(cycleStats.activeMembers) }} 人</div>
            <div class="kpi-trend down">
              <ArrowDownOutlined /> 1.8%
            </div>
          </div>
        </div>
      </a-card>
    </div>

    <div class="main-section">
      <a-card title="会员活跃度分布" class="chart-card">
        <PlotlyChart
          :data="activityChartData"
          :layout="activityChartLayout"
          height="380px"
        />
      </a-card>

      <a-card title="流失预警名单" class="churn-card">
        <template #extra>
          <a-tag color="red">共 {{ churnTotal }} 人</a-tag>
        </template>
        <a-table
          :columns="churnColumns"
          :data-source="churnMembers"
          :pagination="{ pageSize: 6 }"
          size="middle"
          row-key="memberId"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'memberName'">
              <div class="member-info">
                <a-avatar :style="{ backgroundColor: '#E8A0BF' }" size="small">
                  {{ record.memberName.charAt(0) }}
                </a-avatar>
                <span>{{ record.memberName }}</span>
              </div>
            </template>
            <template v-else-if="column.key === 'level'">
              <a-tag :color="getLevelColor(record.level)">
                {{ getLevelText(record.level) }}
              </a-tag>
            </template>
            <template v-else-if="column.key === 'daysSinceLastVisit'">
              <span class="days-text">
                <WarningOutlined v-if="record.daysSinceLastVisit >= 60" class="warning-icon" />
                {{ record.daysSinceLastVisit }} 天
              </span>
            </template>
            <template v-else-if="column.key === 'totalRecharge'">
              ¥{{ formatNumber(record.totalRecharge) }}
            </template>
            <template v-else-if="column.key === 'action'">
              <a-button type="link" size="small">
                <PhoneOutlined /> 联系回访
              </a-button>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import {
  CalendarOutlined,
  ReloadOutlined,
  TeamOutlined,
  UserOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  WarningOutlined,
  PhoneOutlined,
} from '@ant-design/icons-vue'
import PlotlyChart from '@/components/charts/PlotlyChart.vue'
import { memberApi } from '@/api/member'
import { useFilter } from '@/composables/useFilter'
import type { MemberCycleStats, ChurnMember, ChurnResponse } from '@/types'

const { filterParams } = useFilter()

const cycleStats = ref<MemberCycleStats>({
  avgRechargeCycle: 45,
  rechargeRate: 0.68,
  totalMembers: 5280,
  activeMembers: 3680,
  newMembers: 0,
})
const churnMembers = ref<ChurnMember[]>([])
const churnTotal = ref(0)

const churnColumns = [
  { title: '会员姓名', key: 'memberName', dataIndex: 'memberName' },
  { title: '所属门店', dataIndex: 'storeName', key: 'storeName' },
  { title: '未到店天数', dataIndex: 'daysSinceLastVisit', key: 'daysSinceLastVisit' },
  { title: '累计充值', dataIndex: 'totalRecharge', key: 'totalRecharge' },
  { title: '到店次数', dataIndex: 'totalVisits', key: 'totalVisits' },
  { title: '流失等级', key: 'level', dataIndex: 'level', width: 100 },
  { title: '操作', key: 'action', width: 100 },
]

const activityChartData = computed(() => {
  const active = cycleStats.value.activeMembers
  const inactive = cycleStats.value.totalMembers - active
  const newMembers = cycleStats.value.newMembers || 0
  const churned = churnTotal.value

  return [
    {
      x: ['活跃会员', '沉睡会员', '新增会员', '流失预警'],
      y: [active, inactive, newMembers, churned],
      type: 'bar',
      marker: {
        color: ['#E8A0BF', '#DDD6FE', '#A7D8B0', '#F5C6A5'],
        borderRadius: [6, 6, 0, 0],
      },
      text: [
        `${active}人 (${((active / (cycleStats.value.totalMembers || 1)) * 100).toFixed(1)}%)`,
        `${inactive}人 (${((inactive / (cycleStats.value.totalMembers || 1)) * 100).toFixed(1)}%)`,
        `${newMembers}人`,
        `${churned}人`,
      ],
      textposition: 'outside',
      hovertemplate: '<b>%{x}</b><br>人数: %{y}人<extra></extra>',
    },
  ]
})

const activityChartLayout = {
  margin: { l: 60, r: 30, t: 20, b: 40 },
  xaxis: {
    showgrid: false,
    zeroline: false,
  },
  yaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    title: {
      text: '人数',
      font: { size: 12, color: '#666' },
    },
  },
  showlegend: false,
}

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

function getLevelColor(level: string): string {
  const colors: Record<string, string> = {
    high: 'red',
    medium: 'orange',
    low: 'gold',
  }
  return colors[level] || 'default'
}

function getLevelText(level: string): string {
  const texts: Record<string, string> = {
    high: '高风险',
    medium: '中风险',
    low: '低风险',
  }
  return texts[level] || '未知'
}

async function loadData() {
  try {
    const [cycle, churnResp] = await Promise.all([
      memberApi.getMemberCycle(filterParams.value),
      memberApi.getChurnMembers(filterParams.value),
    ])
    cycleStats.value = cycle
    churnTotal.value = churnResp.total
    churnMembers.value = churnResp.list
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
.member-lifecycle {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.kpi-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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

.main-section {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
}

.chart-card,
.churn-card {
  min-height: 460px;
}

.member-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.days-text {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #ff4d4f;
  font-weight: 500;
}

.warning-icon {
  font-size: 16px;
}

@media (max-width: 1200px) {
  .kpi-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 900px) {
  .main-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .kpi-cards {
    grid-template-columns: 1fr;
  }
}
</style>
