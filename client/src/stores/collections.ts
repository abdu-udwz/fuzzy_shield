import { getCollections } from '@/services/collections'
import { defineStore } from 'pinia'

export const useCollectionsStore = defineStore('collections', () => {

  const collections = ref<string[]>([])

  async function fetch() {
    try {
      const { data } = await getCollections()
      if (data.value != null) {
        collections.value = data.value
      }
    } catch (error) {
      alert('Error fetching collections')
    }
  }

  void fetch()

  return {
    collections,
    fetch,
  }

})
