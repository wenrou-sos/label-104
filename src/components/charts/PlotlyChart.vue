<template>
  <div ref="chartRef" :style="{ width: width, height: height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount, nextTick } from 'vue'
import Plotly from 'plotly.js-dist-min'

interface PlotlyData {
  x?: any[]
  y?: any[]
  z?: any[]
  type?: string
  name?: string
  mode?: string
  marker?: any
  line?: any
  text?: string[]
  hoverinfo?: string
  values?: any[]
  labels?: string[]
  hole?: number
  orientation?: string
  [key: string]: any
}

interface PlotlyLayout {
  title?: string | any
  xaxis?: any
  yaxis?: any
  yaxis2?: any
  legend?: any
  margin?: any
  paper_bgcolor?: string
  plot_bgcolor?: string
  font?: any
  showlegend?: boolean
  barmode?: string
  shapes?: any[]
  annotations?: any[]
  [key: string]: any
}

interface PlotlyConfig {
  responsive?: boolean
  displayModeBar?: boolean
  displaylogo?: boolean
  [key: string]: any
}

const props = withDefaults(
  defineProps<{
    data: PlotlyData[]
    layout?: PlotlyLayout
    config?: PlotlyConfig
    width?: string
    height?: string
  }>(),
  {
    width: '100%',
    height: '400px',
  }
)

const chartRef = ref<HTMLDivElement | null>(null)
let plotlyInstance: any = null

const defaultLayout: PlotlyLayout = {
  margin: { l: 50, r: 20, t: 40, b: 40 },
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
  font: {
    family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    size: 12,
    color: '#333',
  },
  legend: {
    bgcolor: 'rgba(255,255,255,0)',
    bordercolor: 'rgba(0,0,0,0)',
  },
}

const defaultConfig: PlotlyConfig = {
  responsive: true,
  displayModeBar: false,
  displaylogo: false,
}

async function renderChart() {
  if (!chartRef.value) return

  const mergedLayout = { ...defaultLayout, ...props.layout }
  const mergedConfig = { ...defaultConfig, ...props.config }

  plotlyInstance = await Plotly.newPlot(
    chartRef.value,
    props.data as any,
    mergedLayout,
    mergedConfig
  )
}

function handleResize() {
  if (chartRef.value && plotlyInstance) {
    Plotly.Plots.resize(chartRef.value)
  }
}

watch(
  () => [props.data, props.layout],
  () => {
    nextTick(() => {
      renderChart()
    })
  },
  { deep: true }
)

onMounted(() => {
  renderChart()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (chartRef.value) {
    Plotly.purge(chartRef.value)
  }
})

defineExpose({
  resize: handleResize,
})
</script>
