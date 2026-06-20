import { ref, computed } from 'vue'
import type { Store } from '@/types'
import { storeApi } from '@/api/store'
import { mockData } from '@/api/mock'

const startDate = ref('2024-01-01')
const endDate = ref('2024-06-30')
const selectedStoreIds = ref<string[]>([])
const stores = ref<Store[]>([])
let storesLoaded = false

export function useFilter() {
  const storeOptions = computed(() =>
    stores.value.map(s => ({ label: s.storeName, value: s.storeId }))
  )

  async function loadStores() {
    if (storesLoaded) return
    try {
      const data = await storeApi.getStores()
      stores.value = data
      if (data.length > 0 && selectedStoreIds.value.length === 0) {
        selectedStoreIds.value = data.map(s => s.storeId)
      }
    } catch {
      stores.value = mockData.stores
      selectedStoreIds.value = mockData.stores.map(s => s.storeId)
    }
    storesLoaded = true
  }

  const filterParams = computed(() => ({
    startDate: startDate.value,
    endDate: endDate.value,
    storeIds: selectedStoreIds.value.join(','),
  }))

  return {
    startDate,
    endDate,
    selectedStoreIds,
    stores,
    storeOptions,
    loadStores,
    filterParams,
  }
}

export default useFilter
