import { createFetch } from '@vueuse/core'

export const useAPI = createFetch({
  baseUrl: '/api',
  combination: 'chain',
  options: {
    updateDataOnError: true,
    beforeFetch({ options }) {
      options.headers = {
        'Content-Type': 'application/json'
      }

      return { options }
    }
  }
})
