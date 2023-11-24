import {defineStore} from 'pinia'

export const useRootStore = defineStore('root', {
  state() {
    return {
      apiUrl: import.meta.env.MODE === 'production' ? 'https://publicpulse.flint3s.ru' : 'http://localhost:5000'
    }
  },
  actions: {}
})
