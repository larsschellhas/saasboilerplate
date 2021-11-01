import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "Home" */ '../views/Home.vue'),
    meta: {
      allowAnonymous: true
    }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import(/* webpackChunkName: "Dashboard" */ '../views/Dashboard.vue'),
    meta: {
      allowAnonymous: false
    }
  },
  {
    path: '/login/',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login/Login.vue'),
    meta: {
      allowAnonymous: true
    }
  },
  {
    path: '/register/',
    name: 'Register',
    component: () => import(/* webpackChunkName: "register" */ '../views/Login/Register.vue'),
    meta: {
      allowAnonymous: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (!to.meta.allowAnonymous && !store.getters['user/isLoggedIn']) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (to.meta.allowAnonymous && store.getters['user/isLoggedIn']) {
    next({
      name: 'Dashboard'
    })
  } else {
    next()
  }
})

export default router
