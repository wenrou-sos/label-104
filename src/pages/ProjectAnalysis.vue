<template>
  <div class="project-analysis">
    <div class="top-section">
      <a-card title="销售额占比" class="pie-card">
        <PlotlyChart
          :data="pieChartData"
          :layout="pieChartLayout"
          height="380px"
        />
      </a-card>

      <a-card title="毛利率对比" class="bar-card">
        <PlotlyChart
          :data="marginChartData"
          :layout="marginChartLayout"
          height="380px"
        />
      </a-card>
    </div>

    <a-card title="项目四象限分析" class="matrix-card">
      <div class="matrix-legend">
        <div class="legend-item">
          <span class="legend-dot star"></span>
          <span>明星项目 (高销售高毛利)</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot question"></span>
          <span>问题项目 (低销售高毛利)</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot cow"></span>
          <span>现金牛 (高销售低毛利)</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot dog"></span>
          <span>瘦狗项目 (低销售低毛利)</span>
        </div>
      </div>
      <PlotlyChart
        :data="matrixChartData"
        :layout="matrixChartLayout"
        height="450px"
      />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import PlotlyChart from '@/components/charts/PlotlyChart.vue'
import { projectApi } from '@/api/project'
import { useFilter } from '@/composables/useFilter'
import type { ProjectSales, ProjectMatrix, ProjectMargin } from '@/types'

const { filterParams } = useFilter()

const salesData = ref<ProjectSales[]>([])
const marginData = ref<ProjectMargin[]>([])
const matrixData = ref<ProjectMatrix[]>([])

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

const pieChartData = computed(() => {
  return [
    {
      values: salesData.value.map(d => d.salesAmount),
      labels: salesData.value.map(d => d.projectName),
      type: 'pie',
      hole: 0.5,
      marker: {
        colors: chartColors,
      },
      textinfo: 'label+percent',
      textposition: 'outside',
      hovertemplate: '<b>%{label}</b><br>销售额: ¥%{value:,.0f}<br>占比: %{percent}<extra></extra>',
    },
  ]
})

const totalSales = computed(() =>
  salesData.value.reduce((sum, item) => sum + item.salesAmount, 0)
)

const pieChartLayout = computed(() => ({
  margin: { l: 20, r: 20, t: 10, b: 20 },
  showlegend: false,
  annotations: [
    {
      text: '总销售额',
      x: 0.5,
      y: 0.55,
      xref: 'paper',
      yref: 'paper',
      showarrow: false,
      font: { size: 14, color: '#666' },
    },
    {
      text: `¥${formatNumber(totalSales.value)}`,
      x: 0.5,
      y: 0.42,
      xref: 'paper',
      yref: 'paper',
      showarrow: false,
      font: { size: 20, color: '#E8A0BF', weight: 'bold' },
    },
  ],
}))

const marginChartData = computed(() => {
  const source = marginData.value.length > 0 ? marginData.value : salesData.value
  const sorted = [...source].sort(
    (a: any, b: any) => Number(b.grossMarginRate ?? 0) - Number(a.grossMarginRate ?? 0)
  )
  return [
    {
      x: sorted.map((d: any) => (Number(d.grossMarginRate ?? 0) * 100).toFixed(1) + '%'),
      y: sorted.map((d: any) => d.projectName),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: sorted.map((_, i) => chartColors[i % chartColors.length]),
        borderRadius: [0, 6, 6, 0],
      },
      text: sorted.map((d: any) => `¥${formatNumber(Number(d.grossMargin ?? 0))}`),
      textposition: 'auto',
      hovertemplate:
        '<b>%{y}</b><br>毛利率: %{x}<br>毛利额: ¥%{text}<extra></extra>',
    },
  ]
})

const marginChartLayout = {
  margin: { l: 120, r: 30, t: 20, b: 40 },
  xaxis: {
    gridcolor: '#f0f0f0',
    zeroline: false,
    title: {
      text: '毛利率',
      font: { size: 12, color: '#666' },
    },
  },
  yaxis: {
    showgrid: false,
    zeroline: false,
  },
  showlegend: false,
}

const matrixChartData = computed(() => {
  const quadrants = [
    { name: '明星项目', color: '#E8A0BF', projects: [] as ProjectMatrix[] },
    { name: '问题项目', color: '#6B5B95', projects: [] as ProjectMatrix[] },
    { name: '瘦狗项目', color: '#ccc', projects: [] as ProjectMatrix[] },
    { name: '现金牛', color: '#F5C6A5', projects: [] as ProjectMatrix[] },
  ]

  matrixData.value.forEach(p => {
    const idx = p.quadrant - 1
    if (idx >= 0 && idx < 4) {
      quadrants[idx].projects.push(p)
    }
  })

  return quadrants.map(q => ({
    x: q.projects.map(p => p.salesAmount),
    y: q.projects.map(p => p.grossMarginRate * 100),
    mode: 'markers+text',
    name: q.name,
    text: q.projects.map(p => p.projectName),
    textposition: 'top center',
    marker: {
      size: 18,
      color: q.color,
      opacity: 0.8,
      line: { color: '#fff', width: 2 },
    },
    hovertemplate:
      '<b>%{text}</b><br>销售额: ¥%{x:,.0f}<br>毛利率: %{y:.1f}%<extra></extra>',
  }))
})

const matrixChartLayout = computed(() => {
  const maxSales = Math.max(...matrixData.value.map(p => p.salesAmount)) * 1.1
  const minSales = 0
  const maxMargin =
    Math.max(...matrixData.value.map(p => p.grossMarginRate * 100)) * 1.1
  const minMargin = 0

  const midSales = (maxSales + minSales) / 2
  const midMargin = (maxMargin + minMargin) / 2

  return {
    margin: { l: 60, r: 30, t: 20, b: 50 },
    xaxis: {
      gridcolor: '#f0f0f0',
      zeroline: false,
      title: {
        text: '销售额 (元)',
        font: { size: 12, color: '#666' },
      },
      range: [minSales, maxSales],
      tickformat: ',.0f',
    },
    yaxis: {
      gridcolor: '#f0f0f0',
      zeroline: false,
      title: {
        text: '毛利率 (%)',
        font: { size: 12, color: '#666' },
      },
      range: [minMargin, maxMargin],
    },
    shapes: [
      {
        type: 'line',
        x0: midSales,
        y0: minMargin,
        x1: midSales,
        y1: maxMargin,
        line: { color: '#ddd', width: 1, dash: 'dash' },
      },
      {
        type: 'line',
        x0: minSales,
        y0: midMargin,
        x1: maxSales,
        y1: midMargin,
        line: { color: '#ddd', width: 1, dash: 'dash' },
      },
    ],
    annotations: [
      {
        x: maxSales * 0.75,
        y: maxMargin * 0.85,
        text: '⭐ 明星项目',
        showarrow: false,
        font: { size: 14, color: '#E8A0BF' },
      },
      {
        x: maxSales * 0.25,
        y: maxMargin * 0.85,
        text: '❓ 问题项目',
        showarrow: false,
        font: { size: 14, color: '#6B5B95' },
      },
      {
        x: maxSales * 0.25,
        y: maxMargin * 0.15,
        text: '🐶 瘦狗项目',
        showarrow: false,
        font: { size: 14, color: '#999' },
      },
      {
        x: maxSales * 0.75,
        y: maxMargin * 0.15,
        text: '🐄 现金牛',
        showarrow: false,
        font: { size: 14, color: '#F5C6A5' },
      },
    ],
    showlegend: false,
  }
})

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

async function loadData() {
  try {
    const [sales, margin, matrix] = await Promise.all([
      projectApi.getProjectSales(filterParams.value),
      projectApi.getProjectMargin(filterParams.value),
      projectApi.getProjectMatrix(filterParams.value),
    ])
    salesData.value = sales
    marginData.value = margin
    matrixData.value = matrix
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
.project-analysis {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.top-section {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
}

.pie-card,
.bar-card {
  min-height: 440px;
}

.matrix-card {
  min-height: 520px;
}

.matrix-legend {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-dot.star {
  background: #E8A0BF;
}

.legend-dot.question {
  background: #6B5B95;
}

.legend-dot.cow {
  background: #F5C6A5;
}

.legend-dot.dog {
  background: #ccc;
}

@media (max-width: 900px) {
  .top-section {
    grid-template-columns: 1fr;
  }
}
</style>
