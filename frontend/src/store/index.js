import { createStore } from 'vuex'
import { storeApiPlugin } from '@/api/axiosConfig'
import user from './modules/user'

export default createStore({
  modules: {
    user
  },
  plugins: [
    storeApiPlugin
  ]
})
